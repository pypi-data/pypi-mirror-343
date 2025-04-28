import json
from typing import Dict, Any

import redis

from ..config.config import Config
from ..exceptions.errors import SDKInitError, SendMessageError

try:
    redis_url = f"redis://{Config.REDIS_USER}:{Config.REDIS_PASSWORD}@{Config.REDIS_HOST}:{Config.REDIS_PORT}/{Config.REDIS_DB}"
    pool = redis.ConnectionPool.from_url(
        redis_url,
        decode_responses=True,  # 自动解码响应为字符串
        socket_connect_timeout=5,  # 连接超时5秒
        socket_keepalive=True,
        max_connections=100,  # 最大连接数
        health_check_interval=30,  # 健康检查间隔
    )
except Exception:
    pool = None


class RedisService:
    """
    Redis 服务类, 提供 Redis 连接池管理和基础操作功能
    """

    def __init__(self):
        if pool is None:
            raise SDKInitError("Redis 连接池初始化失败")

        try:
            self.client = redis.Redis(connection_pool=pool)
        except Exception as e:
            raise SDKInitError(f"Redis 初始化失败: {e}")

    def publish_realtime(self, target_user_id: str, data: Dict[str, Any]):
        """
        发布实时消息到指定用户的频道

        Args:
            target_user_id: 目标用户ID
            data: 要发送的消息数据

        Raises:
            SendMessageError: 当消息发送失败时抛出
        """
        channel = f"realtime:user:{target_user_id}"
        try:
            self.client.publish(channel, json.dumps(data))
        except Exception as e:
            raise SendMessageError(f"发送实时消息失败: {e}")

    def generate_seq(self, user_id: str) -> int:
        """
        基于 Redis 的 INCR 机制生成单用户的单调递增 seq 值

        Args:
            user_id: 用户ID

        Returns:
            int: 生成的序列号

        Raises:
            SendMessageError: 当序列号生成失败时抛出
        """
        key = f"seq:user:{user_id}"
        try:
            return self.client.incr(key)
        except Exception as e:
            raise SendMessageError(f"Redis 生成 seq 失败: {e}")
