"""Maintainer script: build exercises/*.py from solutions/*.py by blanking out function bodies.

Keeps module docstrings, imports, constants and each function's docstring, so the lessons live in
one place. Run `python tools/make_exercises.py` after editing a solution; `--check` fails if stale.
Functions whose name starts with "_" or that appear in KEEP stay as written (they're given helpers).
"""
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEEP = {"count_tokens"}  # helpers handed to the learner, not part of the exercise


def blank(source: str, number: str) -> str:
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_") and node.name not in KEEP:
            doc = node.body[0] if ast.get_docstring(node) else None
            todo = ast.parse(f'raise NotImplementedError("Exercise {number}: write {node.name}()")').body
            node.body = ([doc] if doc else []) + todo
    return "# Your code goes here. Run `python -m agentkata` to check it.\n" + ast.unparse(tree) + "\n"


def main() -> int:
    stale = []
    for sol in sorted((ROOT / "solutions").glob("ex*.py")):
        target = ROOT / "exercises" / sol.name
        text = blank(sol.read_text(encoding="utf-8"), sol.name[2:4])
        if "--check" in sys.argv:
            if not target.exists() or target.read_text(encoding="utf-8") != text:
                stale.append(target.name)
        else:
            target.write_text(text, encoding="utf-8")
    if stale:
        print("Stale exercises (run tools/make_exercises.py):", ", ".join(stale))
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
