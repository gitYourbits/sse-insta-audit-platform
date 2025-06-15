"""
Helper functions and decorators for the Instagram Follower Audit Tool.
This module provides utility functions and decorators for common operations.
"""

import functools
import time
import random
import asyncio
from typing import Any, Callable, TypeVar, cast, Optional, Union, Tuple, Dict
import logging
from datetime import datetime
import json

# Type variable for decorator typing
F = TypeVar('F', bound=Callable[..., Any])

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Callable[[F], F]:
    """
    Retry decorator with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry
        
    Returns:
        Decorated function
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(current_delay)
                        current_delay *= backoff
                        logging.warning(
                            f"Retry attempt {attempt + 1} for {func.__name__}"
                        )
            
            raise last_exception
        
        return cast(F, wrapper)
    return decorator

def async_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 10.0,
    exceptions: Union[type, Tuple[type, ...]] = Exception,
    on_retry: Optional[Callable[[Exception, int], None]] = None,
    retry_on_result: Optional[Callable[[Any], bool]] = None,
    retry_on_exception: Optional[Callable[[Exception], bool]] = None,
    logger: Optional[logging.Logger] = None
) -> Callable[[F], F]:
    """Async retry decorator with exponential backoff, jitter, and comprehensive error handling.
    
    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        base_delay: Base delay between retries in seconds (default: 1.0)
        max_delay: Maximum delay between retries in seconds (default: 10.0)
        exceptions: Exception(s) to catch and retry (default: Exception)
        on_retry: Optional callback function called on retry with (exception, attempt_number)
        retry_on_result: Optional callback function to determine if retry is needed based on result
        retry_on_exception: Optional callback function to determine if retry is needed based on exception
        logger: Optional logger instance for retry logging
        
    Returns:
        Decorated async function with retry logic
        
    Example:
        @async_retry(
            max_attempts=3,
            base_delay=1.0,
            max_delay=10.0,
            exceptions=(ConnectionError, TimeoutError),
            on_retry=lambda e, attempt: print(f"Retry {attempt} due to {e}")
        )
        async def my_async_function():
            # Function implementation
    """
    if logger is None:
        logger = logging.getLogger(__name__)
        
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            last_result = None
            
            for attempt in range(max_attempts):
                try:
                    result = await func(*args, **kwargs)
                    
                    # Check if we should retry based on result
                    if retry_on_result and retry_on_result(result):
                        last_result = result
                        if attempt < max_attempts - 1:
                            delay = _calculate_delay(attempt, base_delay, max_delay)
                            logger.warning(
                                f"Retry {attempt + 1}/{max_attempts} for {func.__name__} "
                                f"due to result condition. Next attempt in {delay:.2f}s"
                            )
                            await asyncio.sleep(delay)
                            continue
                        break
                    
                    return result
                    
                except exceptions as e:
                    last_exception = e
                    
                    # Check if we should retry based on exception
                    if retry_on_exception and not retry_on_exception(e):
                        raise
                    
                    if attempt < max_attempts - 1:
                        delay = _calculate_delay(attempt, base_delay, max_delay)
                        
                        # Log retry attempt
                        logger.warning(
                            f"Retry {attempt + 1}/{max_attempts} for {func.__name__} "
                            f"after {delay:.2f}s due to {type(e).__name__}: {str(e)}"
                        )
                        
                        # Call on_retry callback if provided
                        if on_retry:
                            try:
                                on_retry(e, attempt + 1)
                            except Exception as callback_error:
                                logger.error(
                                    f"Error in on_retry callback: {str(callback_error)}"
                                )
                        
                        await asyncio.sleep(delay)
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}. "
                            f"Last error: {type(e).__name__}: {str(e)}"
                        )
                        raise
            
            # If we have a last result from retry_on_result, return it
            if last_result is not None:
                return last_result
                
            # If we have a last exception, raise it
            if last_exception:
                raise last_exception
                
            return None
            
        return cast(F, wrapper)
    return decorator

def _calculate_delay(attempt: int, base_delay: float, max_delay: float) -> float:
    """Calculate delay with exponential backoff and jitter.
    
    Args:
        attempt: Current attempt number
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        
    Returns:
        Calculated delay in seconds
    """
    # Exponential backoff with jitter
    delay = min(
        base_delay * (2 ** attempt) + random.uniform(0, 1),
        max_delay
    )
    return delay

def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    """Format a timestamp for display.
    
    Args:
        timestamp: Optional datetime to format (defaults to current time)
        
    Returns:
        Formatted timestamp string
    """
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def safe_divide(numerator: float, denominator: float) -> float:
    """
    Safely divide two numbers, returning 0 if denominator is 0.
    
    Args:
        numerator: The numerator
        denominator: The denominator
        
    Returns:
        Result of division or 0 if denominator is 0
    """
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return 0.0

def normalize_score(score: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """
    Normalize a score to be between min_val and max_val.
    
    Args:
        score: Score to normalize
        min_val: Minimum value of normalized score
        max_val: Maximum value of normalized score
        
    Returns:
        Normalized score
    """
    return max(min_val, min(max_val, score))

def safe_json_loads(json_str: str) -> Dict[str, Any]:
    """Safely parse JSON string with error handling.
    
    Args:
        json_str: JSON string to parse
        
    Returns:
        Parsed JSON data as dictionary
        
    Raises:
        ValueError: If JSON parsing fails
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON data: {str(e)}")

def validate_required_fields(data: Dict[str, Any], required_fields: list[str]) -> None:
    """Validate that required fields are present in data.
    
    Args:
        data: Dictionary to validate
        required_fields: List of required field names
        
    Raises:
        ValueError: If any required field is missing
    """
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}") 