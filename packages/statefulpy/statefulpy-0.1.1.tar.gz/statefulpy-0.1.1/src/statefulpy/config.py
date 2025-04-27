"""
Configuration management for StatefulPy.
"""
import copy
import logging
from typing import Dict, Any, Optional, Union, List

logger = logging.getLogger(__name__)

# Default configuration
_DEFAULT_CONFIG: Dict[str, Any] = {
    'backend': 'sqlite',
    'backend_options': {
        'sqlite': {
            'db_path': 'statefulpy.db',
            'serializer': 'pickle',
        },
        'redis': {
            'redis_url': 'redis://localhost:6379/0',
            'serializer': 'pickle',
            'prefix': 'statefulpy:',
            'lock_timeout': 30000,  # 30 seconds in milliseconds
        }
    },
    'debug': False,
}

# Global configuration
_CONFIG: Dict[str, Any] = copy.deepcopy(_DEFAULT_CONFIG)


def set_backend(backend: str, **options) -> None:
    """
    Set the default backend and its options for StatefulPy.
    
    This function updates the global configuration to use the specified backend
    and options for all @stateful decorators that don't specify a backend.
    
    Args:
        backend: Backend type ('sqlite' or 'redis')
        **options: Backend-specific options
    
    Raises:
        ValueError: If the backend type is unknown
    
    Examples:
        >>> set_backend('redis', redis_url='redis://localhost:6379/0')
        >>> set_backend('sqlite', db_path='app_state.db', serializer='json')
    """
    global _CONFIG
    
    if backend not in _DEFAULT_CONFIG['backend_options']:
        valid_backends = list(_DEFAULT_CONFIG['backend_options'].keys())
        raise ValueError(
            f"Unknown backend type: {backend}. "
            f"Valid backends are: {', '.join(valid_backends)}"
        )
    
    # Update backend type
    _CONFIG['backend'] = backend
    
    # Update backend options
    for key, value in options.items():
        if backend in _CONFIG['backend_options']:
            _CONFIG['backend_options'][backend][key] = value
        else:
            _CONFIG['backend_options'][backend] = {key: value}
    
    logger.debug(f"Default backend set to {backend} with options {options}")


def get_config() -> Dict[str, Any]:
    """
    Get the current configuration.
    
    Returns:
        A deep copy of the current configuration dictionary
    """
    return copy.deepcopy(_CONFIG)


def get_backend_options(backend: Optional[str] = None) -> Dict[str, Any]:
    """
    Get options for the specified backend or the default backend.
    
    Args:
        backend: Backend type to get options for (default: current default backend)
    
    Returns:
        A dictionary of backend options
        
    Raises:
        ValueError: If the backend type is unknown
    """
    opts = _CONFIG.get("backend_options", {})  # now typed as dict
    if backend:
        return opts.get(backend, {})
    return opts


def reset_config() -> None:
    """
    Reset the configuration to defaults.
    
    This function is primarily useful for testing.
    """
    global _CONFIG
    _CONFIG = copy.deepcopy(_DEFAULT_CONFIG)


def some_function() -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    # Fill result with values
    return result


def another_function() -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    # Fill result with values
    return result
