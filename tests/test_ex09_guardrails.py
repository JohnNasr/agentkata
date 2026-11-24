import inspect

from agentkata import load

ex = load("ex09_guardrails")


def delete_file(path: str) -> str:
    """Delete a file."""
    deleted.append(path)
    return f"deleted {path}"


def read_file(path: str) -> str:
    """Read a file."""
    return "contents"


deleted: list = []
TOOLS = {"delete_file": delete_file, "read_file": read_file}


def test_denied_tool_does_not_run():
    deleted.clear()
    guarded = ex.guard_tools(TOOLS, {"delete_file"}, approve=lambda name, args: False)
    assert guarded["delete_file"](path="a.txt") == "Denied: the user did not allow 'delete_file'."
    assert deleted == []


def test_approved_tool_runs_and_approve_sees_arguments():
    deleted.clear()
    asked = []
    guarded = ex.guard_tools(TOOLS, {"delete_file"}, approve=lambda name, args: asked.append((name, args)) or True)
    assert guarded["delete_file"](path="b.txt") == "deleted b.txt"
    assert asked == [("delete_file", {"path": "b.txt"})]


def test_safe_tools_untouched_and_input_unchanged():
    guarded = ex.guard_tools(TOOLS, {"delete_file"}, approve=lambda n, a: False)
    assert guarded["read_file"] is read_file
    assert TOOLS["delete_file"] is delete_file
    assert guarded is not TOOLS


def test_wrapper_looks_like_the_original():
    wrapped = ex.guard_tools(TOOLS, {"delete_file"}, approve=lambda n, a: True)["delete_file"]
    assert wrapped.__name__ == "delete_file"
    assert wrapped.__doc__ == "Delete a file."
    assert list(inspect.signature(wrapped).parameters) == ["path"]
