import threading
from typing import Callable

import pytest
from pytest_mock import MockerFixture

from kakaowork.ratelimit import RateLimiter
from tests import Clock, _async_return


class TestRateLimiter:
    def test_rate_limiter_properties(self, timer):
        limiter = RateLimiter(capacity=10, refill_rate=1.0)
        assert limiter._capacity == 10
        assert limiter._refill_rate == 1.0
        assert callable(limiter._timer)
        assert isinstance(limiter._lock, type(threading.RLock()))
        assert isinstance(limiter._last_refill_time, float)
        assert limiter._tokens == 10

    def test_rate_limiter_reset(self, mocker: MockerFixture, timer: Clock):
        mocker.patch('time.perf_counter', side_effect=timer)

        limiter = RateLimiter(capacity=1, refill_rate=1.0)

        timer.tick(1.0)
        limiter.reset()
        assert limiter._capacity == 1
        assert limiter._refill_rate == 1.0
        assert limiter._last_refill_time == 1.0
        assert limiter._tokens == 1

        timer.tick(1.0)
        limiter.reset(capacity=10, refill_rate=10.0)
        assert limiter._capacity == 10
        assert limiter._refill_rate == 10.0
        assert limiter._last_refill_time == 2.0
        assert limiter._tokens == 10

    def test_rate_limiter_limit_exceeded(self, mocker: MockerFixture, timer: Clock):
        mock_timer = mocker.patch('time.perf_counter', side_effect=timer)

        limiter = RateLimiter(capacity=1, refill_rate=1.0)
        assert limiter.limit() == 0.0
        assert limiter.limit() == 1.0
        assert mock_timer.called and mock_timer.call_count == 3

    def test_rate_limiter_limit_not_exceeded(self, mocker: MockerFixture, timer: Clock):
        mock_timer = mocker.patch('time.perf_counter', side_effect=timer)

        limiter = RateLimiter(capacity=1, refill_rate=1.0)
        assert limiter.limit() == 0.0
        timer.tick(1.0)
        assert limiter.limit() == 0.0
        assert mock_timer.called and mock_timer.call_count == 3

    def test_rate_limiter_context_manager_exceeded(self, mocker: MockerFixture, timer: Clock):
        mock_sleep = mocker.patch('time.sleep', return_value=None)
        mock_timer = mocker.patch('time.perf_counter', side_effect=timer)

        limiter = RateLimiter(capacity=1, refill_rate=1.0)

        with limiter:
            pass

        mock_sleep.assert_not_called()
        assert mock_timer.called and mock_timer.call_count == 2

        with limiter:
            pass

        mock_sleep.asset_called_once_with(1.0)
        assert mock_timer.called and mock_timer.call_count == 3

    def test_rate_limiter_context_manager_not_exceeded(self, mocker: MockerFixture, timer: Clock):
        mock_sleep = mocker.patch('time.sleep', return_value=None)
        mock_timer = mocker.patch('time.perf_counter', side_effect=timer)

        limiter = RateLimiter(capacity=1, refill_rate=1.0)

        with limiter:
            pass

        mock_sleep.assert_not_called()
        assert mock_timer.called and mock_timer.call_count == 2

        timer.tick(1.0)

        with limiter:
            pass

        mock_sleep.assert_not_called()
        assert mock_timer.called and mock_timer.call_count == 3

    @pytest.mark.asyncio
    async def test_rate_limiter_async_context_manager_exceeded(self, mocker: MockerFixture, timer: Clock):
        mock_sleep = mocker.patch('asyncio.sleep', return_value=_async_return(None))
        mock_timer = mocker.patch('time.perf_counter', side_effect=timer)

        limiter = RateLimiter(capacity=1, refill_rate=1.0)

        async with limiter:
            pass

        mock_sleep.assert_not_called()
        assert mock_timer.called and mock_timer.call_count == 2

        async with limiter:
            pass

        mock_sleep.assert_called_once_with(1.0)
        assert mock_timer.called and mock_timer.call_count == 3

    @pytest.mark.asyncio
    async def test_rate_limiter_async_context_manager_not_exceeded(self, mocker: MockerFixture, timer: Clock):
        mock_sleep = mocker.patch('asyncio.sleep', return_value=_async_return(None))
        mock_timer = mocker.patch('time.perf_counter', side_effect=timer)

        limiter = RateLimiter(capacity=1, refill_rate=1.0)

        async with limiter:
            pass

        mock_sleep.assert_not_called()
        assert mock_timer.called and mock_timer.call_count == 2

        timer.tick(1.0)

        async with limiter:
            pass

        mock_sleep.assert_not_called()
        assert mock_timer.called and mock_timer.call_count == 3

    def test_rate_limiter_decorator_exceeded(self, mocker: MockerFixture, timer: Clock):
        mock_sleep = mocker.patch('time.sleep', return_value=None)
        mock_timer = mocker.patch('time.perf_counter', side_effect=timer)

        limiter = RateLimiter(capacity=1, refill_rate=1.0)

        @limiter
        def call(a, *, b):
            return a, b

        call(1, b=2)
        call(1, b=2)
        mock_sleep.assert_called_once_with(1.0)
        assert mock_timer.called and mock_timer.call_count == 3

    def test_rate_limiter_decorator_not_exceeded(self, mocker: MockerFixture, timer: Clock):
        mock_sleep = mocker.patch('time.sleep', return_value=None)
        mock_timer = mocker.patch('time.perf_counter', side_effect=timer)

        limiter = RateLimiter(capacity=1, refill_rate=1.0)

        @limiter
        def call(a, *, b):
            return a, b

        call(1, b=2)
        timer.tick(1.0)
        call(1, b=2)
        mock_sleep.assert_not_called()
        assert mock_timer.called and mock_timer.call_count == 3
