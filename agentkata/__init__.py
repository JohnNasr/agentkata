"""agentkata: learn to build AI agents from scratch, one failing test at a time."""
import importlib
import os

from .models import FakeModel, OllamaModel

__all__ = ["FakeModel", "OllamaModel", "load"]
__version__ = "0.1.0"


def load(name: str):
    """Import an exercise module: yours from exercises/, or the reference one when KATA_SOLUTIONS=1."""
    package = "solutions" if os.environ.get("KATA_SOLUTIONS") == "1" else "exercises"
    return importlib.import_module(f"{package}.{name}")
