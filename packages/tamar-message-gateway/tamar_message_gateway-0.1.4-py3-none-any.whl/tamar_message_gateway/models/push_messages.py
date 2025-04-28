import os
from enum import IntEnum, Enum
import uuid

from sqlalchemy import Column, String, Integer, JSON, TIMESTAMP, BigInteger, func

from .base import Base


class PushType(IntEnum):
    RELIABLE_MESSAGE = 1
    COMMAND_REQUEST = 2


class MessageStatus(str, Enum):
    PENDING = "PENDING"
    DELIVERING = "DELIVERING"
    FINISHED = "FINISHED"
    TIMED_OUT = "TIMED_OUT"
    REQUEST_DELIVERED = "REQUEST_DELIVERED"


class PushMessage(Base):
    __bind_key__ = "saas" if os.getenv("APP_ENV") == "production" else "test"
    __tablename__ = "push_messages"

    id = Column(
        String, primary_key=True, default=lambda: str(uuid.uuid4()), comment="主键id"
    )
    sender_type = Column(
        String,
        nullable=True,
        default="server",
        comment="调用端类型，枚举值: server, client",
    )
    sender_id = Column(
        String,
        nullable=True,
        comment="调用端ID，如果是server端触发的，传对应服务名的唯一标识，client触发的传client_id",
    )
    target_user_id = Column(String, nullable=False, comment="目标用户ID")
    push_type = Column(
        Integer,
        nullable=False,
        comment="推送类型，枚举值：1: reliable_message, 2: command_request",
    )
    seq = Column(
        BigInteger,
        nullable=True,
        comment="用户消息顺序号，同一用户内单调递增",
    )
    payload = Column(JSON, nullable=True, comment="消息体")
    status = Column(
        String,
        nullable=False,
        default=MessageStatus.PENDING,
        comment="消息状态，枚举值：PENDING, DELIVERING, REQUEST_DELIVERED, FINISHED, TIMED_OUT",
    )
    command_request_id = Column(
        String,
        nullable=True,
        comment="command请求ID，用于Request-Response模式下匹配响应",
    )
    command_response = Column(JSON, nullable=True, comment="来自接收端的响应结果")
    command_response_queue = Column(
        String, nullable=True, comment="command响应队列名称"
    )
    nonce = Column(
        String,
        nullable=True,
        default=lambda: str(uuid.uuid4()),
        comment="幂等性nonce，用于避免消息重复处理",
    )
    expired_at = Column(TIMESTAMP, nullable=True, comment="command超时时间")
    retry_interval = Column(Integer, nullable=True, comment="command重试间隔(ms)")
    delivering_at = Column(TIMESTAMP, nullable=True, comment="开始投递时间")
    request_delivered_at = Column(
        TIMESTAMP, nullable=True, comment="接收端 ACK 确认送达时间"
    )
    finished_at = Column(TIMESTAMP, nullable=True, comment="任务最终完成时间")
    created_at = Column(
        TIMESTAMP, server_default=func.current_timestamp(), comment="创建时间"
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment="修改时间",
    )
    deleted_at = Column(TIMESTAMP, nullable=True, default=None, comment="删除时间")
