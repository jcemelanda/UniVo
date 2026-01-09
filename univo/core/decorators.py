"""Utilities for UniVo.

Primarily contains logging and performance tracking decorators.
"""
import functools
import logging
import time
from collections.abc import Callable
from typing import Any, TypeVar

# Global logger for the application
logger = logging.getLogger("univo")

F = TypeVar("F", bound=Callable[..., Any])

def log_interaction[F: Callable[..., Any]](func: F) -> F:
    """Decorator that logs function calls, arguments, and execution time.
    
    Used primarily in the service layer to trace user interactions 
    and debug data flows.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        
        # Format args for logging (simplified)
        # Skip 'self' (args[0])
        call_args = ", ".join(
            [repr(a) for a in args[1:]] + 
            [f"{k}={v!r}" for k, v in kwargs.items()]
        )
        
        logger.debug(f"Action: {func.__name__}({call_args})")
        
        try:
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start_time
            logger.debug(f"Success: {func.__name__} in {duration:.4f}s")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
            
    return wrapper  # type: ignore[return-value]
