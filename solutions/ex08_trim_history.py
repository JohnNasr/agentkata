"""Exercise 08: memory that fits

Models have a context limit, and every token you send costs time (and money with paid APIs).
Long chats must be trimmed. The simple, common approach: keep the system message, then keep
the most recent messages that fit in the budget, and drop the oldest.

One trap: a "tool" message only makes sense right after the assistant message that asked for it.
If trimming cuts between them, the model sees a tool result out of nowhere. Never keep an orphan.
"""


def count_tokens(message: dict) -> int:
    """Rough token count: about 4 characters per token, plus a little overhead per message."""
    return len(message.get("content") or "") // 4 + 4


def trim_history(messages: list[dict], max_tokens: int, count=count_tokens) -> list[dict]:
    """Return a trimmed copy of `messages` that fits in `max_tokens` (measured with `count`).

    - If the first message is a system message, always keep it (its tokens count toward the budget).
    - Then keep as many of the most recent messages as fit, in their original order.
      Stop at the first (newest-to-oldest) message that doesn't fit; don't skip over it.
    - Always keep the last message, even if it alone is over budget.
    - Remove "tool" messages from the start of the kept part (their assistant request was dropped).
    """
    head = messages[:1] if messages and messages[0]["role"] == "system" else []
    rest = messages[len(head):]
    budget = max_tokens - sum(count(m) for m in head)
    kept: list[dict] = []
    for msg in reversed(rest):
        if kept and count(msg) > budget:
            break
        kept.insert(0, msg)
        budget -= count(msg)
    while len(kept) > 1 and kept[0]["role"] == "tool":
        kept.pop(0)
    return head + kept
