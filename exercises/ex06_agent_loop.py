# Your code goes here. Run `python -m agentkata` to check it.
"""Exercise 06: the agent loop

This is the heart of every AI agent, from tiny scripts to Claude Code:

    1. send the messages (and tool descriptions) to the model
    2. if the reply has no tool calls, it is the final answer: stop
    3. otherwise run each tool, add the results to the messages, and go back to 1

A tool result goes back as a message with role "tool":

    {"role": "tool", "name": "add", "content": "5"}

Add a step limit, or a confused model can loop forever (and spend forever).
"""
from agentkata import load

def run_agent(model, tools: dict, user_input: str, system: str='You are a helpful assistant.', max_steps: int=5) -> str:
    """Run the loop above and return the final answer text.

    - Describe every tool with function_to_tool (exercise 03) and pass the list as model.chat(messages, tools=...).
    - Append each assistant reply to the messages as-is, then one "tool" message per tool call
      (use run_tool from exercise 05).
    - After `max_steps` model calls without a final answer, return
      "Stopped: reached max_steps (<max_steps>) without a final answer."
    """
    raise NotImplementedError('Exercise 06: write run_agent()')
