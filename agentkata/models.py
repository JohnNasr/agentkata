"""Two models with the same interface, so exercise code works with either.

    reply = model.chat(messages, tools=None)

`messages` is a list of {"role": "system" | "user" | "assistant" | "tool", "content": str, ...}.
The reply is always a dict:

    {"role": "assistant", "content": "text", "tool_calls": [{"name": "add", "arguments": {"a": 1}}]}

`tool_calls` is an empty list when the model just answers.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request


def _reply(content: str = "", tool_calls: list | None = None) -> dict:
    return {"role": "assistant", "content": content, "tool_calls": tool_calls or []}


class FakeModel:
    """A scripted model for tests. Give it the replies it should return, in order.

    Each scripted reply is a string (plain answer), a dict (full reply, e.g. with tool_calls),
    or an Exception instance (raised, to simulate a network error).
    """

    def __init__(self, replies: list):
        self.replies = list(replies)
        self.calls: list[dict] = []  # every request, so tests can check what you sent

    def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        self.calls.append({"messages": [dict(m) for m in messages], "tools": tools})
        if not self.replies:
            raise RuntimeError("FakeModel ran out of scripted replies: your code called chat() too many times.")
        nxt = self.replies.pop(0)
        if isinstance(nxt, Exception):
            raise nxt
        if isinstance(nxt, str):
            return _reply(nxt)
        return _reply(nxt.get("content", ""), nxt.get("tool_calls"))


class OllamaModel:
    """A real local model through Ollama (https://ollama.com). Free, offline, no API key.

    Install Ollama, run `ollama pull qwen3:4b` (or any model with tool support), then use
    OllamaModel("qwen3:4b").
    """

    def __init__(self, model: str = "qwen3:4b", host: str = "http://localhost:11434", timeout: float = 120):
        self.model, self.host, self.timeout = model, host.rstrip("/"), timeout

    def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        body = {"model": self.model, "messages": [self._to_ollama(m) for m in messages], "stream": False}
        if tools:
            body["tools"] = [{"type": "function", "function": t} for t in tools]
        req = urllib.request.Request(f"{self.host}/api/chat", data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                msg = json.load(resp)["message"]
        except urllib.error.URLError as e:
            raise ConnectionError(f"Could not reach Ollama at {self.host}. Is it running? ({e})") from e
        calls = [{"name": c["function"]["name"], "arguments": c["function"].get("arguments") or {}}
                 for c in msg.get("tool_calls") or []]
        return _reply(msg.get("content", ""), calls)

    @staticmethod
    def _to_ollama(m: dict) -> dict:
        out = {"role": m["role"], "content": m.get("content", "")}
        if m.get("tool_calls"):
            out["tool_calls"] = [{"function": {"name": c["name"], "arguments": c["arguments"]}}
                                 for c in m["tool_calls"]]
        return out
