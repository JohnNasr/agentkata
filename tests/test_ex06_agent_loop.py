from agentkata import FakeModel, load

ex = load("ex06_agent_loop")


def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def call(name, **arguments):
    return {"tool_calls": [{"name": name, "arguments": arguments}]}


def test_answer_without_tools():
    model = FakeModel(["Hello!"])
    assert ex.run_agent(model, {"add": add}, "hi") == "Hello!"


def test_uses_a_tool_then_answers():
    model = FakeModel([call("add", a=2, b=3), "2 + 3 = 5"])
    assert ex.run_agent(model, {"add": add}, "what is 2+3?") == "2 + 3 = 5"
    second = model.calls[1]["messages"]
    assert second[-1] == {"role": "tool", "name": "add", "content": "5"}
    assert second[-2]["tool_calls"] == [{"name": "add", "arguments": {"a": 2, "b": 3}}]


def test_sends_tool_descriptions():
    model = FakeModel(["ok"])
    ex.run_agent(model, {"add": add}, "hi")
    assert model.calls[0]["tools"][0]["name"] == "add"
    assert model.calls[0]["messages"][0]["role"] == "system"


def test_errors_go_back_to_the_model():
    model = FakeModel([call("multiply", a=2, b=3), "Sorry, I can only add."])
    assert ex.run_agent(model, {"add": add}, "2*3?") == "Sorry, I can only add."
    assert model.calls[1]["messages"][-1]["content"].startswith("Error: unknown tool 'multiply'")


def test_step_limit():
    model = FakeModel([call("add", a=1, b=1)] * 3)
    assert ex.run_agent(model, {"add": add}, "loop", max_steps=3) == \
        "Stopped: reached max_steps (3) without a final answer."
    assert len(model.calls) == 3
