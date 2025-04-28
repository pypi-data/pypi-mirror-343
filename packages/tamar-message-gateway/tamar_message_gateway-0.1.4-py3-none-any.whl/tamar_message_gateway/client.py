import uuid
from typing import Dict, Any
from datetime import datetime, timedelta
from concurrent.futures import Future
import concurrent.futures

from .config.config import Config
from .exceptions.errors import CommandTimeoutError
from .core.redis_service import RedisService
from .core.mysql_service import MySQLService
from .core.rabbitmq_service import RabbitMQService
from .models.push_messages import PushType


class MessageGatewaySDK:
    def __init__(self, **kwargs):
        """
        初始化客户端
        支持通过 kwargs 覆盖 Config 中的配置
        """
        Config.override(**kwargs)
        Config.validate_required_configs()
        self.redis = RedisService()
        self.mysql = MySQLService()
        self.rabbitmq = RabbitMQService()

    def send_realtime_message(
        self, target_user_id: str, payload: Dict[str, Any]
    ) -> str:
        """
        发送实时消息
        仅面向在线用户, 不保证送达
        """
        self.redis.publish_realtime(target_user_id, payload)

    def send_reliable_message(
        self,
        target_user_id: str,
        payload: Dict[str, Any],
        sender_type: str = None,
        sender_id: str = None,
    ) -> str:
        """
        发送可靠消息
        在线推送 + 离线补偿, 确保 At Least Once 投递
        """
        message_id = self.mysql.create_push_message(
            target_user_id=target_user_id,
            push_type=PushType.RELIABLE_MESSAGE.value,
            payload=payload,
            sender_type=sender_type,
            sender_id=sender_id,
        )
        self.rabbitmq.publish_message(message_id)
        return message_id

    def send_command_message(
        self,
        target_user_id: str,
        type: str,
        data: Dict[str, Any],
        sender_type: str = None,
        sender_id: str = None,
        timeout: int | None = None,
        retry_interval: int | None = None,
        wait_for_response: bool = True,
    ) -> Dict[str, Any] | str:
        """
        发送命令消息
        在线推送 + 离线补偿, 确保 At Least Once 投递
        如果 wait_for_response=True, 阻塞直到拿到响应或超时
        如果 wait_for_response=False, 发送后立即返回 message_id
        """
        timeout = timeout or Config.DEFAULT_TIMEOUT
        retry_interval = retry_interval or Config.DEFAULT_RETRY_INTERVAL
        request_id = str(uuid.uuid4())

        message_id = self.mysql.create_push_message(
            target_user_id=target_user_id,
            push_type=PushType.COMMAND_REQUEST.value,
            payload={
                "type": type,
                "data": data,
            },
            request_id=request_id,
            sender_type=sender_type,
            sender_id=sender_id,
            expired_at=datetime.now() + timedelta(seconds=timeout),
            retry_interval=retry_interval,
        )

        self.rabbitmq.publish_message(message_id, request_id)

        if not wait_for_response:
            return message_id

        future = Future()
        self.rabbitmq.register_future(request_id, future)
        try:
            try:
                return future.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                raise CommandTimeoutError("等待 command_response 超时")
        finally:
            self.rabbitmq.unregister_future(request_id)

    def close(self):
        self.rabbitmq.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
