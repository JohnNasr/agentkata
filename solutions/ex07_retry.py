"""Exercise 07: retries with backoff

Networks fail and model servers get busy. A good agent retries a failed call a few times,
waiting longer each time ("exponential backoff": 0.5s, 1s, 2s, ...) so it doesn't hammer a
struggling server. But it must NOT retry a bug in your own code: that fails the same way forever.
"""
import time


def with_retry(fn, attempts: int = 3, base_delay: float = 0.5, sleep=time.sleep,
               retry_on: tuple = (ConnectionError, TimeoutError)):
    """Call fn() and return its result, retrying on the exception types in `retry_on`.

    - Before retry number k (k = 0, 1, ...), call sleep(base_delay * 2**k).
    - Try at most `attempts` times in total; if the last try fails, re-raise its exception.
    - Any exception NOT in `retry_on` is raised immediately, without retrying.
    - The tests pass a fake `sleep`, so never call time.sleep directly.
    """
    for k in range(attempts):
        try:
            return fn()
        except retry_on:
            if k == attempts - 1:
                raise
            sleep(base_delay * 2**k)
