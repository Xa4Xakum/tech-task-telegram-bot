import inspect
import functools
from typing import ParamSpec, TypeVar, Callable

from loguru import logger


F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")

LOG_LEVELS = {
    'debug': logger.debug,
    'info': logger.info,
    'warning': logger.warning,
    'error': logger.error,
    'success': logger.success
}


def try_do(
    try_count: int = 1,
    level: str = 'error',
    reraise: bool = False,
) -> Callable[[Callable[F_Spec, F_Return]], Callable[F_Spec, F_Return]]:

    def decorator(func: Callable[F_Spec, F_Return]) -> Callable[F_Spec, F_Return]:

        is_async = inspect.iscoroutinefunction(func)

        @functools.wraps(func)
        async def async_wrapper(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return:
            return await _execute_async(func, args, kwargs, try_count, level, reraise)

        @functools.wraps(func)
        def sync_wrapper(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return:
            return _execute_sync(func, args, kwargs, try_count, level, reraise)

        return async_wrapper if is_async else sync_wrapper

    return decorator


async def _execute_async(
    func, args, kwargs, try_count, level,  reraise
):
    errs = []
    for _ in range(try_count):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            errs.append(e)
            logger.opt(exception=True).log(level.upper(), f"{func.__name__} вызвана с args={args}, kwargs={kwargs}")

    if reraise:
        raise errs[0] or Exception("Какого-то хуя корректно не отработало, но при этом ошибки нет")


def _execute_sync(
    func, args, kwargs, try_count, level, reraise
):
    errs = []
    for _ in range(try_count):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            errs.append(e)
            logger.opt(exception=True).log(level.upper(), f"{func.__name__} вызвана с args={args}, kwargs={kwargs}")

    if reraise:
        raise errs[0] or Exception("Какого-то хуя корректно не отработало, но при этом ошибки нет")
