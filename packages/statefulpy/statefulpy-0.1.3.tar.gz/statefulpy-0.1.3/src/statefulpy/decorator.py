"""
Decorator for making functions stateful with persistent state.
"""
import functools
import inspect
import logging
import atexit
import sys
from typing import Any, Callable, Dict, Optional, TypeVar, cast, Tuple

from statefulpy.backends.base import StateBackend, get_backend

logger = logging.getLogger(__name__)
F = TypeVar('F', bound=Callable[..., Any])

# Track all stateful functions for cleanup
_stateful_functions: Dict[str, Tuple[Callable[..., Any], Any]] = {}

class StateProxy:
    """Proxy class that provides attribute-style access to the underlying state dictionary."""
    
    def __init__(self, state_dict=None):
        object.__setattr__(self, "_state_dict", state_dict or {})
    
    def __getattr__(self, name):
        state_dict = object.__getattribute__(self, "_state_dict")
        if name in state_dict:
            return state_dict[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        state_dict = object.__getattribute__(self, "_state_dict")
        state_dict[name] = value
    
    def __delattr__(self, name):
        state_dict = object.__getattribute__(self, "_state_dict")
        if name in state_dict:
            del state_dict[name]
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
            
    def get_state_dict(self):
        return object.__getattribute__(self, "_state_dict")
    
    def update_from_dict(self, new_state):
        object.__setattr__(self, "_state_dict", new_state or {})

    def __contains__(self, key):
        return key in self.get_state_dict()
    
    def __getitem__(self, key):
        return self.get_state_dict()[key]
    
    def __setitem__(self, key, value):
        self.get_state_dict()[key] = value
    
    def __delitem__(self, key):
        del self.get_state_dict()[key]
    
    def __iter__(self):
        return iter(self.get_state_dict())

def stateful_decorator(
    backend=None, 
    serializer=None, 
    reentrant=False, 
    save_on_exit=True, 
    cache=True, 
    **backend_kwargs  # <-- Added to capture extra arguments such as db_path, function_id, etc.
):
    """
    Decorator that adds persistent state to a function.
    
    Args:
        backend: Name of the backend to use ('sqlite' or 'redis')
        **backend_kwargs: Additional backend parameters (e.g., db_path)
    
    Returns:
        Decorated function with persistent state
    """
    if serializer is None:
        serializer = "json"
    
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        # Allow override of the state key using a 'function_id' kwarg
        if 'function_id' in backend_kwargs:
            key = backend_kwargs.pop('function_id')
        else:
            if "<locals>" in func.__qualname__:
                key = f"{func.__module__}.{inspect.stack()[1].function}"
            else:
                key = f"{func.__module__}.{func.__name__}"
        
        # Initialize backend with extra keyword arguments
        backend_instance = get_backend(backend, serializer=serializer, **backend_kwargs)
        
        state_dict = backend_instance.load_state(key) or {}
        state_proxy = StateProxy(state_dict)
        
        _stateful_functions[key] = (func, backend_instance)
        
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            backend_instance.acquire_lock(key)
            try:
                fresh_state = backend_instance.load_state(key)
                if fresh_state:
                    state_proxy.update_from_dict(fresh_state)
                    for k, v in state_proxy.get_state_dict().items():
                        if not hasattr(wrapper, k):
                            setattr(wrapper, k, v)
                result = func(*args, **kwargs)
                if not hasattr(wrapper, "state"):
                    wrapper.state = state_proxy
                backend_instance.save_state(key, state_proxy.get_state_dict())
                logger.debug(f"State for {key} updated: {state_proxy.get_state_dict()}")
                return result
            finally:
                backend_instance.release_lock(key)
        
        if not hasattr(wrapper, "state"):
            wrapper.state = state_proxy
        
        return wrapper
    return decorator

# Register cleanup function
@atexit.register
def _cleanup_stateful_functions():
    """Clean up all stateful functions by ensuring state is saved and locks are released."""
    for fn_id, (func, backend) in _stateful_functions.items():
        try:
            # Ensure the state is saved
            if hasattr(func, 'state'):
                backend.save_state(fn_id, func.state.get_state_dict())
            
            # Release any locks that might be held
            backend.release_lock(fn_id)
        except Exception as e:
            logger.error(f"Error during cleanup of {fn_id}: {e}")

# New alias for backward compatibility
_flush_all_state = _cleanup_stateful_functions

class _Wrapped:
    state: Any  # Add state attribute

stateful = stateful_decorator  # <-- ensures 'stateful' is imported from here
