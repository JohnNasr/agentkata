from agentkata import load

ex = load("ex04_parse_tool_call")


def test_plain_json():
    assert ex.parse_tool_call('{"tool": "weather", "args": {"city": "Berlin"}}') == {
        "name": "weather", "arguments": {"city": "Berlin"}}


def test_inside_fences_with_chatter():
    text = 'Sure! Let me check.\n```json\n{"tool": "weather", "args": {"city": "Erbil"}}\n```\nOne moment.'
    assert ex.parse_tool_call(text) == {"name": "weather", "arguments": {"city": "Erbil"}}


def test_missing_args_means_empty():
    assert ex.parse_tool_call('call {"tool": "now"}') == {"name": "now", "arguments": {}}


def test_skips_broken_and_unrelated_json():
    text = 'first {broken json, then {"note": 1}, then {"tool": "add", "args": {"a": 1}}'
    assert ex.parse_tool_call(text) == {"name": "add", "arguments": {"a": 1}}


def test_no_tool_call():
    assert ex.parse_tool_call("The answer is 42.") is None
    assert ex.parse_tool_call('{"answer": 42}') is None
