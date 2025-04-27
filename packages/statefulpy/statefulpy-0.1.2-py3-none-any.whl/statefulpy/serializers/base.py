"""
Base interface for state serializers.
"""
from abc import ABC, abstractmethod
import typing as t
import importlib
from typing import Any, Dict, Callable, cast


class StateSerializer(ABC):
    """Abstract base class for state serializers."""
    
    @abstractmethod
    def serialize(self, data: dict) -> bytes:
        """Serialize data to bytes."""
        pass
    
    @abstractmethod
    def deserialize(self, data: bytes) -> dict:
        """Deserialize bytes to data."""
        pass


_SERIALIZERS = {
    'pickle': 'statefulpy.serializers.pickle_serializer:PickleSerializer',
    'json': 'statefulpy.serializers.json_serializer:JSONSerializer',
}


def register_serializer(name: str, serializer_path: str) -> None:
    """Register a custom serializer implementation."""
    _SERIALIZERS[name] = serializer_path


def get_serializer(serializer_type: str, **kwargs) -> StateSerializer:
    """Get a serializer instance by type."""
    if serializer_type not in _SERIALIZERS:
        raise ValueError(f"Unknown serializer type: {serializer_type}")
    
    module_path, class_name = _SERIALIZERS[serializer_type].split(':')
    module = importlib.import_module(module_path)
    serializer_class = getattr(module, class_name)
    return cast(StateSerializer, serializer_class(**kwargs))
