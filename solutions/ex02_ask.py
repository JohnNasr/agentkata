"""Exercise 02: calling a model

`model.chat(messages)` sends messages and returns the model's reply as a dict:

    {"role": "assistant", "content": "Paris", "tool_calls": []}

In the tests `model` is a FakeModel that returns scripted replies, so no real AI is needed.
Later you can pass an OllamaModel instead and the same code talks to a real local model.
"""
from agentkata import load


def ask(model, question: str, system: str = "You are a helpful assistant.") -> str:
    """Send one question to the model and return its answer text with surrounding whitespace removed.

    Use build_messages from exercise 01 (load("ex01_messages").build_messages) with an empty history.
    """
    build_messages = load("ex01_messages").build_messages
    reply = model.chat(build_messages(system, [], question))
    return reply["content"].strip()
