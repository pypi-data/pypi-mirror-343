"""
Pickle serializer implementation.

WARNING: The use of pickle is inherently insecure when working with untrusted data.
         For public-facing applications, it is recommended to use the JSON serializer.
"""
import pickle  # Move this import from line 17 to the top
import warnings
from typing import Any, Dict, cast

# Emit a warning when the module is imported
warnings.warn(
    "PickleSerializer is insecure against untrusted input. Consider using JSON serializer for public applications.",
    UserWarning
)

from statefulpy.serializers.base import StateSerializer


class PickleSerializer(StateSerializer):
    """
    A serializer implementation that uses Python's built-in pickle module for
    serializing and deserializing objects.
    
    Warning:
        Pickle is not secure against malicious data. Only use pickle
        serializer with trusted data and when security is not a concern.
        For public-facing applications or when loading untrusted data,
        use JSONSerializer instead.
    """
    
    def __init__(self, protocol=pickle.HIGHEST_PROTOCOL):
        """
        Initialize the pickle serializer.
        
        Args:
            protocol: Pickle protocol version to use
        """
        warnings.warn(
            "PickleSerializer is not secure against malicious data. "
            "Consider using JSONSerializer for untrusted data.",
            UserWarning, stacklevel=2
        )
        self.protocol = protocol
    
    def serialize(self, data: Dict[str, Any]) -> bytes:
        """Serialize data to bytes using pickle."""
        return pickle.dumps(data, protocol=self.protocol)
    
    def deserialize(self, data: bytes) -> Dict[str, Any]:
        """Deserialize bytes to data using pickle."""
        try:
            # Break the long line:
            result = pickle.loads(data)  # deserialize using pickle (assumed short enough)
            return cast(Dict[str, Any], result)
        except (pickle.UnpicklingError, AttributeError, EOFError, ImportError,
                IndexError, TypeError) as e:
            raise ValueError(f"Failed to unpickle data: {e}")
