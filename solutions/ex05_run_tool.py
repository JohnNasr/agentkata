"""Exercise 05: running a tool safely

The model asks for a tool by name with arguments. The model can be wrong: it may invent a tool,
forget an argument, or the tool may crash. An agent must never crash because of that. Instead,
it sends the error back to the model as text, and the model usually fixes its mistake.
"""
import json


def run_tool(tools: dict, call: dict) -> str:
    """Run `call` ({"name": str, "arguments": dict}) using the functions in `tools` (name -> function).

    Always return a string:
    - Unknown tool: "Error: unknown tool '<name>'. Available: <names sorted, comma separated>"
    - The tool raises (including TypeError for wrong arguments): "Error: <ExceptionType>: <message>"
    - Result is a dict or list: json.dumps(result)
    - Anything else: str(result)
    """
    name = call["name"]
    if name not in tools:
        return f"Error: unknown tool '{name}'. Available: {', '.join(sorted(tools))}"
    try:
        result = tools[name](**call.get("arguments", {}))
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"
    return json.dumps(result) if isinstance(result, (dict, list)) else str(result)
