"""Exercise 04: reading a tool call from plain text

Big models return tool calls in a separate field. Small local models often can't, so you ask them
to write JSON in their answer instead, and they wrap it in chatter:

    Sure! I'll look that up.
    ```json
    {"tool": "weather", "args": {"city": "Berlin"}}
    ```

Your job: dig the call out of the text, robustly.
"""
import json


def parse_tool_call(text: str) -> dict | None:
    """Find the first JSON object in `text` that has a "tool" key and return {"name": ..., "arguments": ...}.

    - "arguments" comes from the object's "args" key, or {} if it is missing.
    - The JSON may be inside ``` fences or surrounded by other text.
    - Return None if there is no such object (plain answer, broken JSON, or JSON without "tool").

    Hint: json.JSONDecoder().raw_decode(text, i) parses one JSON value starting at index i
    and ignores whatever comes after it.
    """
    decoder = json.JSONDecoder()
    for i, ch in enumerate(text):
        if ch != "{":
            continue
        try:
            obj, _ = decoder.raw_decode(text, i)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "tool" in obj:
            return {"name": obj["tool"], "arguments": obj.get("args") or {}}
    return None
