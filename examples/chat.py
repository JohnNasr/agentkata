"""Chat with the agent YOU built, using a real local model through Ollama.

    ollama pull qwen3:4b
    python examples/chat.py            # uses your exercises/
    python examples/chat.py --solutions  # uses the reference solutions
    python examples/chat.py --model llama3.2

It has three tools: a calculator, the current time, and writing a note to a file (that one asks you first).
"""
import argparse
import ast
import datetime
import operator
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

ap = argparse.ArgumentParser()
ap.add_argument("--model", default="qwen3:4b")
ap.add_argument("--solutions", action="store_true")
args = ap.parse_args()
if args.solutions:
    os.environ["KATA_SOLUTIONS"] = "1"

from agentkata import OllamaModel, load  # noqa: E402

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
       ast.Pow: operator.pow, ast.USub: operator.neg}


def calculate(expression: str) -> float:
    """Evaluate an arithmetic expression like '(2 + 3) * 4'."""
    def ev(node):  # walk the syntax tree instead of eval(), so the model can't run arbitrary code
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
            return OPS[type(node.op)](ev(node.operand))
        raise ValueError("only numbers and + - * / ** are allowed")
    return ev(ast.parse(expression, mode="eval").body)


def current_time() -> str:
    """Get the current local date and time."""
    return datetime.datetime.now().isoformat(timespec="minutes")


def save_note(text: str) -> str:
    """Append a line of text to notes.txt."""
    with open("notes.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")
    return "saved"


def approve(name, kwargs):
    return input(f"\nAllow {name}({kwargs})? [y/N] ").strip().lower() == "y"


tools = load("ex09_guardrails").guard_tools(
    {"calculate": calculate, "current_time": current_time, "save_note": save_note}, {"save_note"}, approve)
run_agent = load("ex06_agent_loop").run_agent
with_retry = load("ex07_retry").with_retry
model = OllamaModel(args.model)
raw_chat = model.chat
# retry only the model call, never the tools, so a network blip can't save a note twice
model.chat = lambda messages, tools=None: with_retry(lambda: raw_chat(messages, tools))

print(f"Agent ready on {args.model}. Try: 'what is 17% of 2340?' or 'save a note that I finished agentkata'. "
      "Empty line to quit.")
while (question := input("\nyou> ").strip()):
    try:
        print("agent>", run_agent(model, tools, question))
    except ConnectionError as e:
        print(f"agent> {e}")
