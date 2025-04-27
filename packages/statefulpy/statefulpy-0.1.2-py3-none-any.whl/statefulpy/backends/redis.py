"""
Redis backend implementation for distributed state storage and locking.
"""
import json
import pickle
import time
import logging
import threading
from typing import Optional, Dict, Any, cast

import redis

from statefulpy.backends.base import StateBackend

logger = logging.getLogger(__name__)


class RedisBackend(StateBackend):
    """Redis backend for distributed state persistence."""
    
    def __init__(self, 
                 redis_url: str = "redis://localhost:6379/0", 
                 serializer: str = "pickle",
                 prefix: str = "statefulpy:",
                 lock_timeout: int = 30000):  # 30 seconds in milliseconds
        """
        Initialize Redis backend.
        
        Args:
            redis_url: Redis connection URL
            serializer: Serialization format ('pickle' or 'json')
            prefix: Key prefix for Redis
            lock_timeout: Lock timeout in milliseconds
        """
        self.redis_url = redis_url
        self.serializer = serializer
        self.prefix = prefix
        self.lock_timeout = lock_timeout
        self._client = None
        # Add type annotations for lock bookkeeping
        self._locks: Dict[str, str] = {}
        self._lock_owners: Dict[str, int] = {}
        self._lock_counter: Dict[str, int] = {}
    
    @property
    def client(self):
        """Lazy-loaded Redis client."""
        if self._client is None:
            self._client = redis.from_url(self.redis_url)
        return self._client
    
    def _get_state_key(self, fn_id: str) -> str:
        """Get the Redis key for a function's state."""
        return f"{self.prefix}state:{fn_id}"
    
    def _get_lock_key(self, fn_id: str) -> str:
        """Get the Redis key for a function's lock."""
        return f"{self.prefix}lock:{fn_id}"
    
    def load_state(self, fn_id: str) -> Optional[Dict[str, Any]]:
        """Load state for the given function ID."""
        try:
            key = self._get_state_key(fn_id)
            data = self.client.get(key)
            
            if data is None:
                return None
            
            if self.serializer == "pickle":
                result = pickle.loads(data)
            elif self.serializer == "json":
                result = json.loads(data.decode('utf-8'))
            else:
                raise ValueError(f"Unsupported serializer: {self.serializer}")
            return cast(Optional[Dict[str, Any]], result)
        except Exception as e:
            logger.error(f"Failed to load state for {fn_id}: {e}")
            return None
    
    def save_state(self, fn_id: str, data: Dict[str, Any]) -> bool:
        """Save state for the given function ID."""
        try:
            key = self._get_state_key(fn_id)
            
            if self.serializer == "pickle":
                serialized_data = pickle.dumps(data)
            elif self.serializer == "json":
                serialized_data = json.dumps(data).encode('utf-8')
            else:
                raise ValueError(f"Unsupported serializer: {self.serializer}")
            
            self.client.set(key, serialized_data)
            return True
        except Exception as e:
            logger.error(f"Failed to save state for {fn_id}: {e}")
            return False
    
    def acquire_lock(self, fn_id: str, timeout: float = 10.0) -> bool:
        """
        Acquire a distributed lock for the given function ID.
        
        Uses Redis SET NX PX pattern for atomic locks.
        This implementation is reentrant - the same thread can acquire
        the lock multiple times without deadlocking.
        """
        current_thread = threading.get_ident()
        
        # If this thread already owns the lock, increment counter and return True
        if fn_id in self._lock_owners and self._lock_owners[fn_id] == current_thread:
            self._lock_counter[fn_id] += 1
            return True
            
        lock_key = self._get_lock_key(fn_id)
        lock_id = f"{time.time()}"
        
        # Try to acquire the lock with timeout
        start_time = time.time()
        while time.time() - start_time < timeout:
            # SET key value NX PX milliseconds
            # NX - only set if key doesn't exist
            # PX - expire after milliseconds
            acquired = self.client.set(
                lock_key, 
                lock_id, 
                nx=True, 
                px=self.lock_timeout
            )
            
            if acquired:
                self._locks[fn_id] = lock_id
                self._lock_owners[fn_id] = current_thread
                self._lock_counter[fn_id] = 1
                return True
            
            # Wait a bit before retrying
            time.sleep(0.1)
        
        return False
    
    def release_lock(self, fn_id: str) -> bool:
        """
        Release the lock for the given function ID.
        
        For reentrant locks, this decrements the counter and only
        releases when the count reaches zero.
        """
        current_thread = threading.get_ident()
        if fn_id in self._lock_owners and self._lock_owners[fn_id] == current_thread:
            self._lock_counter[fn_id] -= 1
            if self._lock_counter[fn_id] > 0:
                return True
            
            lock_key = self._get_lock_key(fn_id)
            lock_id = self._locks.get(fn_id)
            lua_script = """
            if redis.call('get', KEYS[1]) == ARGV[1] then
                return redis.call('del', KEYS[1])
            else
                return 0
            end
            """
            try:
                result = self.client.eval(lua_script, 1, lock_key, lock_id)
                # Clean up internal bookkeeping when lock is fully released
                del self._locks[fn_id]
                del self._lock_owners[fn_id]
                del self._lock_counter[fn_id]
                return bool(result == 1)
            except Exception as e:
                logger.error(f"Failed to release lock for {fn_id}: {e}")
                return False
        return False
    
    def close(self) -> None:
        """Close the Redis connection and release all locks."""
        # Release all locks
        for fn_id in list(self._locks.keys()):
            self.release_lock(fn_id)
        
        # Close the Redis connection
        if self._client is not None:
            self._client.close()
            self._client = None
