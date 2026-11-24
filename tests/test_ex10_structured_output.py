import pytest

from agentkata import FakeModel, load

ex = load("ex10_structured_output")


def test_clean_json():
    model = FakeModel(['{"name": "Ada", "age": 36}'])
    assert ex.ask_json(model, "Who?", ["name", "age"]) == {"name": "Ada", "age": 36}
    first = model.calls[0]["messages"]
    assert first[0]["role"] == "system" and "name" in first[0]["content"] and "age" in first[0]["content"]
    assert first[1] == {"role": "user", "content": "Who?"}


def test_fenced_json():
    model = FakeModel(['```json\n{"city": "Berlin"}\n```'])
    assert ex.ask_json(model, "Where?", ["city"]) == {"city": "Berlin"}


def test_retries_with_feedback_about_missing_keys():
    model = FakeModel(['{"name": "Ada"}', '{"name": "Ada", "age": 36}'])
    assert ex.ask_json(model, "Who?", ["name", "age"]) == {"name": "Ada", "age": 36}
    retry = model.calls[1]["messages"]
    assert retry[-2]["role"] == "assistant"
    assert retry[-1]["role"] == "user" and "age" in retry[-1]["content"]


def test_retries_on_invalid_json():
    model = FakeModel(["Sure! Here you go: name=Ada", '{"name": "Ada"}'])
    assert ex.ask_json(model, "Who?", ["name"]) == {"name": "Ada"}
    assert "not valid JSON" in model.calls[1]["messages"][-1]["content"]


def test_gives_up():
    model = FakeModel(["nope", "[1, 2]", "still no"])
    with pytest.raises(ValueError):
        ex.ask_json(model, "Who?", ["name"], attempts=3)
    assert len(model.calls) == 3
