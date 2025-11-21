"""Rate limiting and circuit breakers for LLM API calls."""

import asyncio
import logging
import time
from collections import deque
from enum import Enum
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered


class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, requests_per_second: float, burst_size: Optional[int] = None):
        """Initialize rate limiter.
        
        Args:
            requests_per_second: Maximum requests per second
            burst_size: Maximum burst size (defaults to requests_per_second)
        """
        self.requests_per_second = requests_per_second
        self.burst_size = burst_size or int(requests_per_second)
        self.tokens = float(self.burst_size)
        self.last_update = time.time()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Acquire a token, waiting if necessary."""
        async with self._lock:
            now = time.time()
            elapsed = now - self.last_update

            # Add tokens based on elapsed time
            self.tokens = min(
                self.burst_size, self.tokens + elapsed * self.requests_per_second
            )
            self.last_update = now

            # Wait if no tokens available
            if self.tokens < 1.0:
                wait_time = (1.0 - self.tokens) / self.requests_per_second
                await asyncio.sleep(wait_time)
                self.tokens = 0.0
                self.last_update = time.time()
            else:
                self.tokens -= 1.0

    def try_acquire(self) -> bool:
        """Try to acquire a token without waiting.
        
        Returns:
            True if token acquired, False otherwise
        """
        now = time.time()
        elapsed = now - self.last_update

        self.tokens = min(
            self.burst_size, self.tokens + elapsed * self.requests_per_second
        )
        self.last_update = now

        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False


class CircuitBreaker:
    """Circuit breaker pattern for resilient API calls."""

    def __init__(
        self,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        timeout: float = 60.0,
        half_open_timeout: float = 30.0,
    ):
        """Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            success_threshold: Number of successes to close circuit from half-open
            timeout: Time in seconds before attempting to close circuit
            half_open_timeout: Time in seconds to wait in half-open state
        """
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout = timeout
        self.half_open_timeout = half_open_timeout

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        self.last_state_change: float = time.time()
        self._lock = asyncio.Lock()

    async def call(self, func: Callable, *args, **kwargs):
        """Call a function with circuit breaker protection.
        
        Args:
            func: Async function to call
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
            
        Raises:
            CircuitBreakerOpenError: If circuit is open
        """
        async with self._lock:
            if self.state == CircuitState.OPEN:
                if time.time() - self.last_state_change > self.timeout:
                    # Try to transition to half-open
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                    self.last_state_change = time.time()
                    logger.info("Circuit breaker transitioning to HALF_OPEN")
                else:
                    raise CircuitBreakerOpenError("Circuit breaker is OPEN")

            elif self.state == CircuitState.HALF_OPEN:
                if time.time() - self.last_state_change > self.half_open_timeout:
                    # Timeout in half-open, go back to open
                    self.state = CircuitState.OPEN
                    self.last_state_change = time.time()
                    logger.warning("Circuit breaker timeout in HALF_OPEN, returning to OPEN")
                    raise CircuitBreakerOpenError("Circuit breaker is OPEN")

        # Attempt the call
        try:
            result = await func(*args, **kwargs)
            await self._record_success()
            return result
        except Exception as e:
            await self._record_failure()
            raise

    async def _record_success(self) -> None:
        """Record a successful call."""
        async with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.success_threshold:
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    self.success_count = 0
                    self.last_state_change = time.time()
                    logger.info("Circuit breaker CLOSED after successful calls")
            elif self.state == CircuitState.CLOSED:
                self.failure_count = 0

    async def _record_failure(self) -> None:
        """Record a failed call."""
        async with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.state == CircuitState.HALF_OPEN:
                # Failure in half-open, go back to open
                self.state = CircuitState.OPEN
                self.last_state_change = time.time()
                logger.warning("Circuit breaker returned to OPEN after failure in HALF_OPEN")

            elif (
                self.state == CircuitState.CLOSED
                and self.failure_count >= self.failure_threshold
            ):
                # Too many failures, open the circuit
                self.state = CircuitState.OPEN
                self.last_state_change = time.time()
                logger.error(f"Circuit breaker OPENED after {self.failure_count} failures")

    def get_state(self) -> dict:
        """Get current circuit breaker state.
        
        Returns:
            Dictionary with state information
        """
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure_time": self.last_failure_time,
        }


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open."""

    pass


class RetryWithBackoff:
    """Retry logic with exponential backoff."""

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
    ):
        """Initialize retry logic.
        
        Args:
            max_retries: Maximum number of retries
            initial_delay: Initial delay in seconds
            max_delay: Maximum delay in seconds
            exponential_base: Base for exponential backoff
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base

    async def call(
        self, func: Callable, *args, retry_on: Optional[Callable] = None, **kwargs
    ):
        """Call a function with retry logic.
        
        Args:
            func: Async function to call
            *args: Function arguments
            retry_on: Optional function to determine if exception should be retried
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
            
        Raises:
            Last exception if all retries fail
        """
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Check if we should retry this exception
                if retry_on and not retry_on(e):
                    raise

                if attempt < self.max_retries:
                    delay = min(
                        self.initial_delay * (self.exponential_base ** attempt),
                        self.max_delay,
                    )
                    logger.warning(
                        f"Retry attempt {attempt + 1}/{self.max_retries} after {delay}s: {e}"
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"All retry attempts exhausted: {e}")
                    raise

        raise last_exception

