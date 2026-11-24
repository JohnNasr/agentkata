"""`python -m agentkata`: run the exercises in order and stop at the first one that fails."""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GREEN, RED, DIM, BOLD, RESET = "\033[32m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"


def paint(code: str, text: str) -> str:
    return f"{code}{text}{RESET}" if sys.stdout.isatty() and "NO_COLOR" not in os.environ else text


def main() -> int:
    tests = sorted((ROOT / "tests").glob("test_ex*.py"))
    only = sys.argv[1] if len(sys.argv) > 1 else None  # e.g. `python -m agentkata 03`
    if only:
        tests = [t for t in tests if t.stem.startswith(f"test_ex{only.zfill(2)}")]
        if not tests:
            print(f"No exercise {only}.")
            return 2
    for i, test in enumerate(tests):
        name = test.stem.removeprefix("test_")
        result = subprocess.run([sys.executable, "-m", "pytest", str(test), "-q", "-x", "--no-header", "--tb=short",
                                 "-p", "no:cacheprovider"], cwd=ROOT, capture_output=True, text=True)
        if result.returncode == 0:
            print(paint(GREEN, "  done ") + name)
            continue
        print(paint(RED, "  todo ") + paint(BOLD, name))
        print(f"\nOpen {paint(BOLD, f'exercises/{name}.py')}, read the docstring, and make this pass:\n")
        print(paint(DIM, trim(result.stdout)))
        print(f"\n{i}/{len(tests)} done. Run `python -m agentkata` again after editing.")
        return 1
    print(paint(GREEN, f"\nAll {len(tests)} exercises pass. You built an agent from scratch.")
          + "\nTry it with a real model: python examples/chat.py")
    return 0


def trim(output: str, keep: int = 25) -> str:
    """Show the assertion that failed, not pytest's whole report."""
    lines = [ln for ln in output.splitlines() if ln.strip() and not ln.startswith(("=", "short test summary"))]
    return "\n".join(lines[-keep:])


if __name__ == "__main__":
    sys.exit(main())
