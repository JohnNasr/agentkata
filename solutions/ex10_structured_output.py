"""Exercise 10: structured output

Programs need data, not prose. You ask the model for JSON, but models sometimes add text,
wrap it in ``` fences, or forget a field. The fix that works: check the answer, and if it's
wrong, tell the model exactly what was wrong and ask again. Models fix their own mistakes well
when you show them the error.
"""
import json


def ask_json(model, prompt: str, required_keys: list[str], attempts: int = 3) -> dict:
    """Ask the model for a JSON object that has every key in `required_keys`, and return it as a dict.

    - Start with a system message that says to reply with only a JSON object with those keys,
      then the user's `prompt`.
    - Accept a reply wrapped in ``` or ```json fences (strip them before parsing).
    - If the reply isn't a JSON object or misses keys: append the bad reply (as the assistant) and a
      user message explaining the problem, then ask again. The explanation must mention the missing
      key names, or say the reply was "not valid JSON".
    - After `attempts` bad replies, raise ValueError.
    """
    messages = [
        {"role": "system", "content": f"Reply with only a JSON object with these keys: {', '.join(required_keys)}."},
        {"role": "user", "content": prompt},
    ]
    for _ in range(attempts):
        reply = model.chat(messages)
        text = reply["content"].strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[-1].rsplit("```", 1)[0]
        try:
            data = json.loads(text)
            problem = None if isinstance(data, dict) else "the reply was not a JSON object"
        except json.JSONDecodeError:
            data, problem = None, "the reply was not valid JSON"
        if problem is None:
            missing = [k for k in required_keys if k not in data]
            if not missing:
                return data
            problem = f"missing keys: {', '.join(missing)}"
        messages.append(reply)
        messages.append({"role": "user", "content": f"That was wrong: {problem}. Reply with only the JSON object."})
    raise ValueError(f"No valid JSON after {attempts} attempts")
