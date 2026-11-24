import pytest

from agentkata import load

ex = load("ex07_retry")


def flaky(failures, exc=ConnectionError):
    state = {"calls": 0}

    def fn():
        state["calls"] += 1
        if state["calls"] <= failures:
            raise exc("try again")
        return "ok"
    return fn, state


def test_succeeds_after_retries_with_backoff():
    fn, state = flaky(2)
    waits = []
    assert ex.with_retry(fn, attempts=3, base_delay=0.5, sleep=waits.append) == "ok"
    assert state["calls"] == 3
    assert waits == [0.5, 1.0]


def test_gives_up_and_reraises():
    fn, state = flaky(5)
    with pytest.raises(ConnectionError):
        ex.with_retry(fn, attempts=3, sleep=lambda s: None)
    assert state["calls"] == 3


def test_does_not_retry_bugs():
    fn, state = flaky(1, exc=KeyError)
    with pytest.raises(KeyError):
        ex.with_retry(fn, attempts=3, sleep=lambda s: None)
    assert state["calls"] == 1


def test_no_sleep_when_first_try_works():
    waits = []
    assert ex.with_retry(lambda: 7, sleep=waits.append) == 7
    assert waits == []
