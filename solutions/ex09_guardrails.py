"""Exercise 09: guardrails

Some tools are dangerous: deleting files, sending email, spending money. An agent should ask a
human before running them. That's the "Allow / Don't allow" prompt you see in coding agents.

You'll wrap the dangerous tools so they check with an `approve` callback first. The wrapped
tool must still look like the original (same name, docstring and parameters), or
function_to_tool from exercise 03 would describe it wrongly to the model.
"""
import functools


def guard_tools(tools: dict, dangerous: set, approve) -> dict:
    """Return a NEW dict of tools where each tool named in `dangerous` asks first.

    - Before running a dangerous tool, call approve(name, kwargs). If it returns True, run the tool.
      If not, return "Denied: the user did not allow '<name>'." without running it.
    - Safe tools are passed through unchanged.
    - Keep the original name, docstring and signature (hint: functools.wraps).
    - Don't change the `tools` dict you were given.
    """
    def guarded(name, fn):
        @functools.wraps(fn)
        def wrapper(**kwargs):
            if approve(name, kwargs):
                return fn(**kwargs)
            return f"Denied: the user did not allow '{name}'."
        return wrapper

    return {name: guarded(name, fn) if name in dangerous else fn for name, fn in tools.items()}
