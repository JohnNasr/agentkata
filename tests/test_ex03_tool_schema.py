from agentkata import load

ex = load("ex03_tool_schema")


def add(a: int, b: int) -> int:
    """Add two numbers.

    More detail that should not be in the description.
    """
    return a + b


def search(query: str, limit: int = 5, exact: bool = False, score: float = 0.5, tags: list = None, raw=None):
    return []


def test_simple_function():
    assert ex.function_to_tool(add) == {
        "name": "add",
        "description": "Add two numbers.",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
            "required": ["a", "b"],
        },
    }


def test_types_defaults_and_missing_docstring():
    tool = ex.function_to_tool(search)
    assert tool["description"] == ""
    assert tool["parameters"]["properties"] == {
        "query": {"type": "string"}, "limit": {"type": "integer"}, "exact": {"type": "boolean"},
        "score": {"type": "number"}, "tags": {"type": "array"}, "raw": {"type": "string"},
    }
    assert tool["parameters"]["required"] == ["query"]
