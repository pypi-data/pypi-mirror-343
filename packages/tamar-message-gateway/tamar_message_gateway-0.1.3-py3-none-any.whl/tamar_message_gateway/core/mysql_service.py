import datetime
from typing import Dict, Any, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..config.config import Config
from ..exceptions.errors import SDKInitError, SendMessageError
from .redis_service import RedisService
from ..models.push_messages import PushType, PushMessage

try:
    database_url = (
        f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@"
        f"{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DB}?charset=utf8mb4"
    )
    engine = create_engine(
        database_url,
        pool_size=10,  # 池中保持的连接数
        max_overflow=5,  # 允许临时超出的连接数
        pool_timeout=30,  # 获取连接的超时时间 (秒)
        pool_recycle=1800,  # 连接回收时间 (秒), 防止连接因空闲过长而失效
        echo=False,  # 是否打印 SQL 语句, 调试时可设为 True
    )
except Exception:
    engine = None

if engine:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    SessionLocal = None


class MySQLService:
    """
    MySQL 服务类, 提供数据库连接池管理和消息存储功能
    """

    def __init__(self):
        if not SessionLocal:
            raise SDKInitError("MySQL 连接池初始化失败")
        self._redis = RedisService()

    def create_push_message(
        self,
        target_user_id: str,
        push_type: int,
        payload: Dict[str, Any],
        request_id: Optional[str] = None,
        sender_type: Optional[str] = None,
        sender_id: Optional[str] = None,
        expired_at: Optional[datetime.datetime] = None,
        retry_interval: Optional[int] = None,
    ) -> str:
        """
        创建并存储新的推送消息

        该方法会创建一个新的推送消息记录, 并将其存储到数据库中
        同时会为消息生成一个单调递增的序列号

        Args:
            target_user_id: 目标用户 ID
            push_type: 消息推送类型
            payload: 消息内容, 包含要发送的具体数据
            request_id: command 请求 ID, 仅在 push_type 为 COMMAND_REQUEST 时使用
            sender_type: 发送者类型, 默认为 "server"
            sender_id: 发送者 ID, 用于标识消息来源
            expired_at: 消息过期时间, 超过此时间消息将不再处理
            retry_interval: 消息重试间隔(毫秒), 用于控制消息重试的时间间隔

        Returns:
            str: 新创建消息的 ID

        Raises:
            SendMessageError: 当消息创建过程中发生错误时抛出
        """
        if not target_user_id:
            raise SendMessageError("target_user_id 不能为空")

        # 验证 push_type 并转换为枚举
        try:
            push_type_enum = PushType(push_type)
        except ValueError:
            raise SendMessageError(f"无效的 push_type: {push_type}")

        # 生成 seq
        seq = self._redis.generate_seq(target_user_id)
        if seq is None:
            raise SendMessageError("生成用户消息 seq 失败")

        new_message = PushMessage(
            sender_type=sender_type or "server",
            sender_id=sender_id,
            target_user_id=target_user_id,
            push_type=push_type_enum,
            seq=seq,
            payload=payload,
            command_request_id=request_id
            if push_type_enum == PushType.COMMAND_REQUEST
            else None,
            expired_at=expired_at,
            retry_interval=retry_interval,
        )

        session = None
        try:
            session = SessionLocal()
            session.add(new_message)
            session.commit()
            return new_message.id
        except Exception as e:
            if session:
                session.rollback()
            raise SendMessageError(f"MySQL 写入 push_messages 失败: {e}")
        finally:
            if session:
                session.close()
