"""
Tests for the stateful decorator.
"""
import os
import tempfile
import unittest
import time
import gc
from unittest import mock

from statefulpy import stateful


class TestStatefulDecorator(unittest.TestCase):
    """Test suite for the stateful decorator."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
    
    def tearDown(self):
        """Clean up test environment."""
        # Force Python garbage collection to help release file locks
        gc.collect()
        
        # Add a small delay to let locks release
        time.sleep(0.1)
        
        # Try to remove the file multiple times with longer delays if needed
        attempts = 0
        max_attempts = 3
        while attempts < max_attempts:
            try:
                if os.path.exists(self.temp_db.name):
                    os.unlink(self.temp_db.name)
                break
            except PermissionError:
                attempts += 1
                if attempts < max_attempts:
                    time.sleep(0.5 * attempts)
                    gc.collect()
                else:
                    print(f"Warning: Could not delete {self.temp_db.name} - file still in use")
    
    def test_stateful_basic(self):
        """Test basic functionality of the stateful decorator."""
        @stateful(backend="sqlite", db_path=self.temp_db.name)
        def counter():
            if not hasattr(counter, 'count'):
                counter.count = 0
            counter.count += 1
            return counter.count
        
        # First call should return 1
        self.assertEqual(counter(), 1)
        # Second call should return 2
        self.assertEqual(counter(), 2)
    
    def test_stateful_persist_and_reload(self):
        """Test that state persists across function instances."""
        # First instance
        @stateful(backend="sqlite", db_path=self.temp_db.name)
        def counter1():
            if not hasattr(counter1, 'count'):
                counter1.count = 0
            counter1.count += 1
            return counter1.count
            
        # Call first instance a few times
        self.assertEqual(counter1(), 1)
        self.assertEqual(counter1(), 2)
        
        # Create a new instance with the same function signature and backend
        @stateful(backend="sqlite", db_path=self.temp_db.name)
        def counter2():
            if not hasattr(counter2, 'count'):
                counter2.count = 0
            counter2.count += 1
            return counter2.count
            
        # The new instance should continue from the previous state
        self.assertEqual(counter2(), 3)
    
    def test_stateful_with_args(self):
        """Test stateful function with arguments."""
        @stateful(backend="sqlite", db_path=self.temp_db.name)
        def adder(x, y=0):
            if not hasattr(adder, 'sum'):
                adder.sum = 0
            adder.sum += x + y
            return adder.sum
        
        self.assertEqual(adder(1), 1)
        self.assertEqual(adder(2), 3)
        self.assertEqual(adder(3, y=4), 10)
    
    def test_stateful_with_complex_state(self):
        """Test stateful function with complex state (dict, list)."""
        @stateful(backend="sqlite", db_path=self.temp_db.name)
        def collector(item=None, category=None):
            if not hasattr(collector, 'items'):
                collector.items = {}
            
            if item and category:
                if category not in collector.items:
                    collector.items[category] = []
                collector.items[category].append(item)
            
            return collector.items
        
        # Add some items
        collector("apple", "fruits")
        collector("banana", "fruits")
        collector("carrot", "vegetables")
        
        # Check state
        expected = {
            "fruits": ["apple", "banana"],
            "vegetables": ["carrot"]
        }
        self.assertEqual(collector(), expected)


if __name__ == "__main__":
    unittest.main()
