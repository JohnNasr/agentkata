from agentkata import load

ex = load("ex05_run_tool")


def add(a: int, b: int) -> int:
    return a + b


def boom():
    raise ValueError("disk on fire")


TOOLS = {"add": add, "boom": boom, "info": lambda: {"ok": True}}


def test_runs_and_returns_string():
    assert ex.run_tool(TOOLS, {"name": "add", "arguments": {"a": 2, "b": 3}}) == "5"


def test_dict_result_is_json():
    assert ex.run_tool(TOOLS, {"name": "info", "arguments": {}}) == '{"ok": true}'


def test_unknown_tool():
    assert ex.run_tool(TOOLS, {"name": "fly", "arguments": {}}) == "Error: unknown tool 'fly'. Available: add, boom, info"


def test_tool_crash_becomes_text():
    assert ex.run_tool(TOOLS, {"name": "boom", "arguments": {}}) == "Error: ValueError: disk on fire"


def test_wrong_arguments_become_text():
    out = ex.run_tool(TOOLS, {"name": "add", "arguments": {"a": 1}})
    assert out.startswith("Error: TypeError:")
