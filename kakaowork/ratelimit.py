import time
import asyncio
from threading import RLock
from typing import Optional, Callable, List, Dict
from functools import wraps


class RateLimiter:
    """Rate limiter class."""
    def __init__(self, *, capacity: int, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of requests per second.
            refill_rate: Rate at which the rate limiter refills its capacity.
        """
        self._capacity = capacity
        self._refill_rate = refill_rate
        self._timer = time.perf_counter  # Ref https://www.webucator.com/article/python-clocks-explained/
        self._lock = RLock()
        self._last_refill_time = self._timer()
        self._tokens = capacity

    def __call__(self, f: Callable):
        """Decorator to rate limit a function.

        Args:
            f: Function to rate limit.
        """
        @wraps(f)
        def wrapper(*args: List, **kwargs: Dict):
            with self:
                return f(*args, **kwargs)

        return wrapper

    def __enter__(self) -> 'RateLimiter':
        """Enter the rate limiter."""
        if self.capacity <= 0:
            return self
        wait_time = self.limit()
        if wait_time > 0.0:
            time.sleep(wait_time)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the rate limiter."""
        pass

    async def __aenter__(self) -> 'RateLimiter':
        """Enter the rate limiter."""
        if self.capacity <= 0:
            return self
        wait_time = self.limit()
        if wait_time > 0.0:
            await asyncio.sleep(wait_time)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the rate limiter."""
        pass

    @property
    def capacity(self) -> int:  # noqa: D102
        with self._lock:
            return self._capacity

    @capacity.setter
    def capacity(self, value: int) -> None:  # noqa: D102
        with self._lock:
            self._capacity = value

    @capacity.deleter
    def capacity(self) -> None:  # noqa: D102
        with self._lock:
            self._capacity = 0

    @property
    def refill_rate(self) -> float:  # noqa: D102
        with self._lock:
            return self._refill_rate

    @refill_rate.setter
    def refill_rate(self, value: float) -> None:  # noqa: D102
        with self._lock:
            self._refill_rate = value

    @refill_rate.deleter
    def refill_rate(self) -> None:  # noqa: D102
        with self._lock:
            self._refill_rate = 0.0

    def reset(self, *, capacity: Optional[int] = None, refill_rate: Optional[float] = None) -> None:
        """Reset the rate limiter.

        Args:
            capacity: A capacity after limiter reset
            refill_rate: A refill rate after limiter reset
        """
        with self._lock:
            if capacity is not None:
                self._capacity = capacity
            if refill_rate is not None:
                self._refill_rate = refill_rate
            self._last_refill_time = self._timer()
            self._tokens = self._capacity

    def limit(self, requests: int = 1) -> float:
        """Limit the rate of requests.

        Args:
            requests: Number of requests

        Returns:
            A float number of seconds to wait before next request
        """
        with self._lock:
            refill_time = self._timer()
            refill_tokens = int((refill_time - self._last_refill_time) / self.refill_rate)
            if refill_tokens > 0:
                self._tokens = min(self._capacity, self._tokens + refill_tokens)
                self._last_refill_time = refill_time

            wait_time = 0.0
            if self._tokens - requests >= 0:
                self._tokens -= requests
            else:
                wait_time = abs(self._tokens - requests) * self.refill_rate
            return wait_time
