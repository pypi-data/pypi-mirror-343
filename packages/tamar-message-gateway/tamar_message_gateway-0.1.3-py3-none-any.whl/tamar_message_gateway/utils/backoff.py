import time
from functools import wraps
from typing import Callable


def backoff(
    max_attempts: int = 5, base: int = 1, factor: int = 2, max_interval: int = 30
):
    """
    简易指数退避装饰器
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            delay = base
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    attempt += 1
                    if attempt >= max_attempts:
                        raise
                    time.sleep(min(delay, max_interval))
                    delay *= factor

        return wrapper

    return decorator
