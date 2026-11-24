# Your code goes here. Run `python -m agentkata` to check it.
"""Exercise 03: describing a tool

Models can't run your code. Instead, you describe your functions ("tools") as JSON, the model
replies "please call add with a=2, b=3", and YOUR code runs it. The description looks like:

    {
        "name": "add",
        "description": "Add two numbers.",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
            "required": ["a", "b"],
        },
    }

This is JSON Schema, the format every major model provider uses for tools.
"""
import inspect
import typing
JSON_TYPES = {str: 'string', int: 'integer', float: 'number', bool: 'boolean', list: 'array', dict: 'object'}

def function_to_tool(fn) -> dict:
    """Build the tool description above from a Python function.

    - name: the function's name.
    - description: the first line of its docstring, or "" if it has none.
    - parameters.properties: one entry per parameter, with the JSON type from JSON_TYPES.
      A parameter with no type hint (or a type not in JSON_TYPES) is "string".
    - parameters.required: the parameters that have no default value, in order.

    Hint: inspect.signature(fn) lists parameters; typing.get_type_hints(fn) gives their types.
    """
    raise NotImplementedError('Exercise 03: write function_to_tool()')
