from agentkata import FakeModel, load

ex = load("ex02_ask")


def test_returns_stripped_answer():
    model = FakeModel(["  Paris \n"])
    assert ex.ask(model, "Capital of France?") == "Paris"


def test_sends_system_and_question():
    model = FakeModel(["ok"])
    ex.ask(model, "Hi?", system="Be kind.")
    assert model.calls[0]["messages"] == [
        {"role": "system", "content": "Be kind."},
        {"role": "user", "content": "Hi?"},
    ]


def test_calls_model_once():
    model = FakeModel(["one"])
    ex.ask(model, "q")
    assert len(model.calls) == 1
