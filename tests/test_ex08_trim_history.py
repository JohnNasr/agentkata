from agentkata import load

ex = load("ex08_trim_history")


def one(m):  # every message costs 1 token, to keep the tests easy to follow
    return 1


def msg(role, content="x"):
    return {"role": role, "content": content}


def test_keeps_system_and_newest():
    history = [msg("system"), msg("user", "1"), msg("assistant", "2"), msg("user", "3"), msg("assistant", "4")]
    assert ex.trim_history(history, 3, count=one) == [history[0], history[3], history[4]]


def test_fits_entirely():
    history = [msg("user"), msg("assistant")]
    assert ex.trim_history(history, 10, count=one) == history


def test_last_message_always_kept():
    history = [msg("system"), msg("user", "huge")]
    assert ex.trim_history(history, 1, count=lambda m: 100 if m["content"] == "huge" else 1) == history


def test_stops_at_first_message_that_does_not_fit():
    history = [msg("user", "a"), msg("user", "big"), msg("user", "b")]
    cost = lambda m: 5 if m["content"] == "big" else 1  # noqa: E731
    assert ex.trim_history(history, 3, count=cost) == [history[2]]


def test_no_orphan_tool_messages():
    history = [msg("system"), msg("user"), {"role": "assistant", "content": "", "tool_calls": [{"name": "t"}]},
               msg("tool", "result"), msg("assistant", "done")]
    trimmed = ex.trim_history(history, 3, count=one)
    assert trimmed == [history[0], history[4]]


def test_does_not_change_input():
    history = [msg("user", "1"), msg("user", "2")]
    ex.trim_history(history, 1, count=one)
    assert len(history) == 2
