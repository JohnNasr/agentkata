from agentkata import load

ex = load("ex01_messages")


def test_order_is_system_history_user():
    history = [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}]
    assert ex.build_messages("Be brief.", history, "2+2?") == [
        {"role": "system", "content": "Be brief."},
        {"role": "user", "content": "hi"},
        {"role": "assistant", "content": "hello"},
        {"role": "user", "content": "2+2?"},
    ]


def test_empty_system_is_skipped():
    assert ex.build_messages("", [], "hey") == [{"role": "user", "content": "hey"}]


def test_history_is_not_changed():
    history = [{"role": "user", "content": "hi"}]
    ex.build_messages("s", history, "again")
    assert history == [{"role": "user", "content": "hi"}]
