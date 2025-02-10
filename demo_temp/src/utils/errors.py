from functools import wraps
from logging import getLogger
from typing import Any, Callable

from pydantic import ValidationError

_logger = getLogger(__name__)


class ConfigLoaderError(Exception): ...


def _make_error_handler(
    message: str, required: bool = True
) -> Callable[..., Any]:
    """Make (factory) a decorator to handle validators ValidationError, TypeError and ValueError
    with a custom message.

    Args:
        message(str): Custom message to send to logger when the exception occurs.
        required(bool): If the field is required or not.

    Returns:
        A decorator that wraps a function in a try-except block and raise ConfigLoaderError.

    """

    def _decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def _wrapper(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
            try:
                result = func(*args, **kwargs)
                if required and result is None:
                    raise ValueError(f"Field {func.__name__} is required")
                return result
            except (ValidationError, TypeError, ValueError) as exc:
                _logger.error(message)
                raise ConfigLoaderError(message) from exc

        return _wrapper

    return _decorator
