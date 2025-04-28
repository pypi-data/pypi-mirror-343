class SDKBaseError(Exception):
    """所有 SDK 异常基类"""


class ConfigError(SDKBaseError):
    """配置错误"""


class SDKInitError(SDKBaseError):
    """初始化失败"""


class SendMessageError(SDKBaseError):
    """发送消息失败"""


class CommandTimeoutError(SDKBaseError):
    """command 超时未响应"""
