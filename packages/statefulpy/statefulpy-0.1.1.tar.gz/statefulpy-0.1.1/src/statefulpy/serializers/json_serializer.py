"""
JSON serializer implementation.
"""
import json
from typing import Any, Dict, cast

from statefulpy.serializers.base import StateSerializer


class JSONSerializer(StateSerializer):
    """Serializer using JSON."""
    
    def __init__(self, **kwargs):
        """
        Initialize the JSON serializer.
        
        Args:
            **kwargs: Additional arguments to pass to json.dumps
        """
        self.kwargs = kwargs
    
    def serialize(self, data: Dict[str, Any]) -> bytes:
        """Serialize data to bytes using JSON."""
        return json.dumps(data, **self.kwargs).encode('utf-8')
    
    def deserialize(self, data: bytes) -> Dict[str, Any]:
        """Deserialize bytes to data using JSON."""
        result = json.loads(data.decode('utf-8'))
        return cast(Dict[str, Any], result)
