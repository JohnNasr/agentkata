# Your code goes here. Run `python -m agentkata` to check it.
"""Exercise 01: messages

Every chat model works on a list of messages. Each message is a dict with a role and content:

    {"role": "system", "content": "You are a helpful assistant."}   # rules for the model
    {"role": "user", "content": "What is 2 + 2?"}                    # what the person typed
    {"role": "assistant", "content": "4"}                            # what the model said

The model has no memory. To "remember" a conversation, you send the whole history every time.
"""

def build_messages(system: str, history: list[dict], user_input: str) -> list[dict]:
    """Return the list to send to the model: the system message, then the history, then the new user message.

    - Skip the system message if `system` is empty.
    - Do not change `history` itself (the caller still owns it). Return a new list.
    """
    raise NotImplementedError('Exercise 01: write build_messages()')
