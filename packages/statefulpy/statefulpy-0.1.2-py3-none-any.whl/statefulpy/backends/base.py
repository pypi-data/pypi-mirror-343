"""
Base interface for state persistence backends.
"""
from abc import ABC, abstractmethod
import typing as t
import importlib
from typing import Any, cast


class StateBackend(ABC):
    """Abstract base class for state persistence backends."""
    
    @abstractmethod
    def load_state(self, fn_id: str) -> t.Optional[dict]:
        """Load state for the given function ID."""
        pass
    
    @abstractmethod
    def save_state(self, fn_id: str, data: dict) -> bool:
        """Save state for the given function ID."""
        pass
    
    @abstractmethod
    def acquire_lock(self, fn_id: str, timeout: float = 10.0) -> bool:
        """Acquire a lock for the given function ID."""
        pass
    
    @abstractmethod
    def release_lock(self, fn_id: str) -> bool:
        """Release the lock for the given function ID."""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close any resources used by the backend."""
        pass


_BACKENDS = {
    'sqlite': 'statefulpy.backends.sqlite:SQLiteBackend',
    'redis': 'statefulpy.backends.redis:RedisBackend',
}


def register_backend(name: str, backend_path: str) -> None:
    """Register a custom backend implementation."""
    _BACKENDS[name] = backend_path


def get_backend(backend_type: str, **kwargs: Any) -> StateBackend:
    """Get a backend instance by type."""
    if backend_type not in _BACKENDS:
        raise ValueError(f"Unknown backend type: {backend_type}")
    
    module_path, class_name = _BACKENDS[backend_type].split(':')
    module = importlib.import_module(module_path)
    backend_class = getattr(module, class_name)
    backend = backend_class(**kwargs)
    return cast(StateBackend, backend)
