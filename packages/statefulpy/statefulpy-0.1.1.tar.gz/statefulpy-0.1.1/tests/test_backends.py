"""
Tests for backend implementations.
"""
import os
import tempfile
import time
import unittest
from unittest import mock

import pytest

from statefulpy.backends.base import get_backend
from statefulpy.backends.sqlite import SQLiteBackend


class TestSQLiteBackend(unittest.TestCase):
    """Test suite for the SQLite backend."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.backend = SQLiteBackend(db_path=self.temp_db.name)
    
    def tearDown(self):
        """Clean up test environment."""
        self.backend.close()
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_save_and_load_state(self):
        """Test saving and loading state."""
        fn_id = "test_function"
        test_data = {"counter": 42, "name": "test"}
        
        # Save state
        result = self.backend.save_state(fn_id, test_data)
        self.assertTrue(result)
        
        # Load state
        loaded_data = self.backend.load_state(fn_id)
        self.assertEqual(loaded_data, test_data)
    
    def test_nonexistent_state(self):
        """Test loading nonexistent state."""
        fn_id = "nonexistent_function"
        result = self.backend.load_state(fn_id)
        self.assertIsNone(result)
    
    def test_acquire_release_lock(self):
        """Test lock acquisition and release."""
        fn_id = "test_lock"
        
        # Acquire lock
        result = self.backend.acquire_lock(fn_id)
        self.assertTrue(result)
        
        # Release lock
        release_result = self.backend.release_lock(fn_id)
        self.assertTrue(release_result)
    
    def test_lock_reentrance(self):
        """Test that locks are reentrant."""
        fn_id = "test_reentrant_lock"
        
        # Acquire lock twice
        first_acquire = self.backend.acquire_lock(fn_id)
        second_acquire = self.backend.acquire_lock(fn_id)
        
        self.assertTrue(first_acquire)
        self.assertTrue(second_acquire)
        
        # Release once - should still be locked
        first_release = self.backend.release_lock(fn_id)
        self.assertTrue(first_release)
        
        # Release again - should be fully unlocked
        second_release = self.backend.release_lock(fn_id)
        self.assertTrue(second_release)


# Skip Redis tests if redis is not installed or not running
try:
    import redis
    from statefulpy.backends.redis import RedisBackend
    
    # Try to connect to Redis
    r = redis.Redis()
    r.ping()
    redis_available = True
except (ImportError, redis.ConnectionError):
    redis_available = False


@pytest.mark.skipif(not redis_available, reason="Redis is not available")
class TestRedisBackend(unittest.TestCase):
    """Test suite for the Redis backend."""
    
    def setUp(self):
        """Set up test environment."""
        self.prefix = f"test:{time.time()}:"
        self.backend = RedisBackend(prefix=self.prefix)
    
    def tearDown(self):
        """Clean up test environment."""
        # Clean up all keys created during the test
        for key in self.backend.client.keys(f"{self.prefix}*"):
            self.backend.client.delete(key)
        self.backend.close()
    
    def test_save_and_load_state(self):
        """Test saving and loading state."""
        fn_id = "test_function"
        test_data = {"counter": 42, "name": "test"}
        
        # Save state
        result = self.backend.save_state(fn_id, test_data)
        self.assertTrue(result)
        
        # Load state
        loaded_data = self.backend.load_state(fn_id)
        self.assertEqual(loaded_data, test_data)
    
    def test_nonexistent_state(self):
        """Test loading nonexistent state."""
        fn_id = "nonexistent_function"
        result = self.backend.load_state(fn_id)
        self.assertIsNone(result)
    
    def test_acquire_release_lock(self):
        """Test lock acquisition and release."""
        fn_id = "test_lock"
        
        # Acquire lock
        result = self.backend.acquire_lock(fn_id)
        self.assertTrue(result)
        
        # Release lock
        release_result = self.backend.release_lock(fn_id)
        self.assertTrue(release_result)
    
    def test_lock_reentrance(self):
        """Test that locks are reentrant."""
        fn_id = "test_reentrant_lock"
        
        # Acquire lock twice
        first_acquire = self.backend.acquire_lock(fn_id)
        second_acquire = self.backend.acquire_lock(fn_id)
        
        self.assertTrue(first_acquire)
        self.assertTrue(second_acquire)
        
        # Release once - should still be locked
        first_release = self.backend.release_lock(fn_id)
        self.assertTrue(first_release)
        
        # Release again - should be fully unlocked
        second_release = self.backend.release_lock(fn_id)
        self.assertTrue(second_release)
