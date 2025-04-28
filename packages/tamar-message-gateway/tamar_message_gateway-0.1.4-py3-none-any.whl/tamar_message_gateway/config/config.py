import os

from ..exceptions.errors import ConfigError


class Config:
    # ---- Redis ----
    REDIS_USER: str = os.getenv("MSG_REDIS_USER")
    REDIS_PASSWORD: str = os.getenv("MSG_REDIS_PASSWORD")
    REDIS_HOST: str = os.getenv("MSG_REDIS_HOST")
    REDIS_PORT: int = int(os.getenv("MSG_REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("MSG_REDIS_DB"))

    # ---- MySQL ----
    MYSQL_HOST: str = os.getenv("MSG_MYSQL_HOST")
    MYSQL_PORT: int = int(os.getenv("MSG_MYSQL_PORT", "3306"))
    MYSQL_USER: str = os.getenv("MSG_MYSQL_USER")
    MYSQL_PASSWORD: str = os.getenv("MSG_MYSQL_PASSWORD")
    MYSQL_DB: str = os.getenv("MSG_MYSQL_DB")

    # ---- RabbitMQ ----
    RABBITMQ_HOST: str = os.getenv("MSG_RABBITMQ_HOST")
    RABBITMQ_PORT: int = int(os.getenv("MSG_RABBITMQ_PORT", "5672"))
    RABBITMQ_USERNAME: str = os.getenv("MSG_RABBITMQ_USERNAME")
    RABBITMQ_PASSWORD: str = os.getenv("MSG_RABBITMQ_PASSWORD")
    RABBITMQ_VHOST: str = os.getenv("MSG_RABBITMQ_VHOST", "/")

    MAIN_EXCHANGE: str = "ws.message.direct.exchange"
    MAIN_ROUTING_KEY: str = "ws.message.direct"

    # ---- Misc ----
    DEFAULT_TIMEOUT: int = 1800  # 单位:秒, 默认 30 分钟
    DEFAULT_RETRY_INTERVAL: int = 60000  # 单位:毫秒, 默认 1 分钟

    @classmethod
    def override(cls, **kwargs):
        """
        允许用户硬传参覆盖
        如果传入的 key 不存在于 Config 类中，则忽略
        """
        for k, v in kwargs.items():
            if hasattr(cls, k):
                setattr(cls, k, v)

    @classmethod
    def validate_required_configs(cls):
        """
        检查必要的配置参数是否已设置
        """
        required_configs = [
            "REDIS_USER",
            "REDIS_PASSWORD",
            "REDIS_HOST",
            "REDIS_DB",
            "MYSQL_HOST",
            "MYSQL_USER",
            "MYSQL_PASSWORD",
            "MYSQL_DB",
            "RABBITMQ_HOST",
            "RABBITMQ_USERNAME",
            "RABBITMQ_PASSWORD",
        ]
        missing_configs = []
        for key in required_configs:
            if getattr(cls, key, None) is None:
                missing_configs.append(key)

        if missing_configs:
            raise ConfigError(f"缺少必要的配置参数: {', '.join(missing_configs)}")
