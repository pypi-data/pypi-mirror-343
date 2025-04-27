"""
StatefulPy - Transparent persistent state management for Python functions.

This library provides decorators and utilities to automatically persist and
recover function-internal state like counters, caches, and partial results.
"""

__version__ = "0.1.0"

# Import core components to make them available at the package level
from statefulpy.decorator import stateful, _flush_all_state
from statefulpy.config import set_backend, get_config

# Register exit handlers for graceful shutdown
import atexit
atexit.register(_flush_all_state)

def flush_state() -> None:
    """Force flush of all pending state to the backend."""
    _flush_all_state()

__all__ = [
    "stateful",
    "set_backend",
    "get_config",
    "flush_state",
]
