import json
import threading
import time
from concurrent.futures import Future

import pika
from pika.exchange_type import ExchangeType

from ..config.config import Config
from ..exceptions.errors import SDKInitError, SendMessageError
from ..utils.backoff import backoff


class RabbitMQService:
    """
    RabbitMQ 服务类, 提供 RabbitMQ 连接池管理和消息发布/消费功能
    """

    def __init__(self):
        try:
            # 连接状态标志
            self._running = True

            # 发布连接
            self._pub_conn = self._connect()
            self._pub_chan = self._pub_conn.channel()
            self._declare_main_exchange(self._pub_chan)

            # 消费连接
            self._consume_conn = self._connect()
            self._consume_chan = self._consume_conn.channel()
            self._reply_queue = self._declare_reply_queue(self._consume_chan)

            # futures 映射, 用于接收 command 响应
            self._futures: dict[str, Future] = {}
            self._lock = threading.Lock()

            # 启动消费线程
            self._consumer_thread = threading.Thread(
                target=self._consume_loop,
                name="command-response-consumer",
                daemon=True,
            )
            self._consumer_thread.start()
        except Exception as e:
            raise SDKInitError(f"RabbitMQ 初始化失败: {e}")

    def _connect(self) -> pika.BlockingConnection:
        """创建到 RabbitMQ 的连接"""
        creds = pika.PlainCredentials(
            Config.RABBITMQ_USERNAME, Config.RABBITMQ_PASSWORD
        )
        return pika.BlockingConnection(
            pika.ConnectionParameters(
                host=Config.RABBITMQ_HOST,
                port=Config.RABBITMQ_PORT,
                virtual_host=Config.RABBITMQ_VHOST,
                credentials=creds,
                heartbeat=60,
                blocked_connection_timeout=300,
            )
        )

    def _declare_main_exchange(self, channel):
        """声明主交换机, 用于发布消息"""
        channel.exchange_declare(
            exchange=Config.MAIN_EXCHANGE,
            exchange_type=ExchangeType.direct,
            durable=True,
        )

    def _declare_reply_queue(self, channel):
        """声明用于接收 RPC 响应的临时队列"""
        result = channel.queue_declare(
            queue="",
            exclusive=True,  # 队列仅限当前连接可见
            auto_delete=True,  # 连接关闭后自动删除
        )
        return result.method.queue

    def _reconnect_consume(self):
        """重新连接消费端"""
        try:
            # 关闭旧连接
            if self._consume_conn and self._consume_conn.is_open:
                try:
                    self._consume_conn.close()
                except Exception:
                    pass

            # 重新建立连接
            self._consume_conn = self._connect()
            self._consume_chan = self._consume_conn.channel()
            self._reply_queue = self._declare_reply_queue(self._consume_chan)
            return True
        except Exception:
            return False

    def _reconnect_publish(self):
        """重新连接发布端"""
        try:
            # 关闭旧连接
            if self._pub_conn and self._pub_conn.is_open:
                try:
                    self._pub_conn.close()
                except Exception:
                    pass

            # 重新建立连接
            self._pub_conn = self._connect()
            self._pub_chan = self._pub_conn.channel()
            self._declare_main_exchange(self._pub_chan)
            return True
        except Exception:
            return False

    def register_future(self, req_id: str, fut: Future) -> None:
        """注册 future, 用于接收 command 响应"""
        with self._lock:
            self._futures[req_id] = fut

    def unregister_future(self, req_id: str) -> None:
        """注销 future"""
        with self._lock:
            if req_id in self._futures:
                self._futures.pop(req_id)

    def _pop_future(self, req_id: str) -> Future | None:
        """从 futures 中移除并返回 future"""
        with self._lock:
            return self._futures.pop(req_id, None)

    @backoff()
    def publish_message(self, message_id: str, req_id: str = None) -> None:
        """
        向主交换机发布消息

        Args:
            message_id: 消息ID
            req_id: 可选的请求ID, 如果提供则启用RPC模式, 使用 reply_to + correlation_id
        """
        # 确保连接可用
        if (
            not self._pub_conn
            or not self._pub_conn.is_open
            or not self._pub_chan
            or not self._pub_chan.is_open
        ):
            if not self._reconnect_publish():
                raise SendMessageError("无法连接到 RabbitMQ 发布端")

        body = json.dumps({"message_id": message_id})

        # 基础属性
        properties = pika.BasicProperties(
            content_type="application/json",
            delivery_mode=2,  # 持久化
        )

        # 如果提供了 req_id, 启用 RPC 模式
        if req_id:
            properties = pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2,  # 持久化
                reply_to=self._reply_queue,
                correlation_id=req_id,
            )

        # 发布消息
        self._pub_chan.basic_publish(
            exchange=Config.MAIN_EXCHANGE,
            routing_key=Config.MAIN_ROUTING_KEY,
            body=body,
            properties=properties,
        )

    def _consume_loop(self):
        def _callback(ch, method, props, body):
            """处理响应消息回调"""
            if not props.correlation_id:
                # 没有关联ID的消息, 无法处理
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

            try:
                req_id = props.correlation_id
                fut = self._pop_future(req_id)

                # 如果找不到对应的 future 或 future 已完成, 可能是超时或重复响应
                if not fut or fut.done():
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    return

                try:
                    response = json.loads(body)
                    fut.set_result(response)
                except Exception as e:
                    fut.set_exception(ValueError(f"无效的响应格式: {str(e)}"))
            except Exception:
                pass
            finally:
                # 确保消息被确认
                ch.basic_ack(delivery_tag=method.delivery_tag)

        while self._running:
            try:
                # 确保连接和通道有效
                if (
                    not self._consume_conn
                    or not self._consume_conn.is_open
                    or not self._consume_chan
                    or not self._consume_chan.is_open
                ):
                    if not self._reconnect_consume():
                        # 重连失败, 等待后重试
                        time.sleep(3)
                        continue

                # 开始消费消息
                self._consume_chan.basic_consume(
                    self._reply_queue, on_message_callback=_callback
                )

                try:
                    # 会进入 Pika 的 I/O 循环, 等待并处理来自 RabbitMQ 的消息。只要连接正常, 程序会一直阻塞在这里
                    self._consume_chan.start_consuming()
                except Exception:
                    pass
            except Exception:
                pass

            # 如果执行到这里, 说明消费过程中断
            # 等待一段时间后尝试重连
            time.sleep(3)

    def close(self, timeout: float = 5.0):
        """线程安全地执行关闭"""
        self._running = False

        # 让消费线程里的 IOLoop 执行 stop_consuming + close
        if self._consume_conn and self._consume_conn.is_open:

            def _graceful_shutdown():
                if self._consume_chan.is_open:
                    try:
                        self._consume_chan.stop_consuming()
                    except Exception:
                        pass
                try:
                    self._consume_conn.close()
                except Exception:
                    pass

            # 把回调排队给 IOLoop
            self._consume_conn.add_callback_threadsafe(_graceful_shutdown)

        # 等待消费线程真正退出（可设置超时）
        if self._consumer_thread.is_alive():
            self._consumer_thread.join(timeout=timeout)

        # 关闭发布连接（同一线程内安全）
        try:
            if self._pub_conn and self._pub_conn.is_open:
                self._pub_conn.close()
        except Exception:
            pass
