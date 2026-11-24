# Your code goes here. Run `python -m agentkata` to check it.
"""Exercise 10: structured output

Programs need data, not prose. You ask the model for JSON, but models sometimes add text,
wrap it in ``` fences, or forget a field. The fix that works: check the answer, and if it's
wrong, tell the model exactly what was wrong and ask again. Models fix their own mistakes well
when you show them the error.
"""
import json

def ask_json(model, prompt: str, required_keys: list[str], attempts: int=3) -> dict:
    """Ask the model for a JSON object that has every key in `required_keys`, and return it as a dict.

    - Start with a system message that says to reply with only a JSON object with those keys,
      then the user's `prompt`.
    - Accept a reply wrapped in ``` or ```json fences (strip them before parsing).
    - If the reply isn't a JSON object or misses keys: append the bad reply (as the assistant) and a
      user message explaining the problem, then ask again. The explanation must mention the missing
      key names, or say the reply was "not valid JSON".
    - After `attempts` bad replies, raise ValueError.
    """
    raise NotImplementedError('Exercise 10: write ask_json()')
