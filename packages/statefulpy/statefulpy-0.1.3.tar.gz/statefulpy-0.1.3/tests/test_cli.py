"""
Tests for the command-line interface.
"""
import os
import tempfile
import unittest
import time
import gc
from unittest import mock

from statefulpy.cli import init_command, migrate_command, healthcheck_command, list_command


class TestCLICommands(unittest.TestCase):
    """Test suite for CLI commands."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.target_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.target_db.close()
    
    def tearDown(self):
        """Clean up test environment."""
        # Force Python garbage collection to help release file locks
        gc.collect()
        
        # Increase delay to allow locks to release
        time.sleep(0.5)
        
        # Try to remove the test files multiple times with extended delays
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                if os.path.exists(self.temp_db.name):
                    os.unlink(self.temp_db.name)
                if os.path.exists(self.target_db.name):
                    os.unlink(self.target_db.name)
                break
            except PermissionError:
                time.sleep(1.0 * (attempt + 1))
                gc.collect()
                if attempt == max_attempts - 1:
                    print("Warning: Could not delete test files - still in use")
    
    def test_init_command(self):
        """Test the init command."""
        # Create a mock args object
        args = mock.Mock()
        args.backend = 'sqlite'
        args.path = self.temp_db.name
        
        # Run the command
        result = init_command(args)
        self.assertEqual(result, 0)
        self.assertTrue(os.path.exists(self.temp_db.name))
    
    def test_migrate_command(self):
        """Test the migrate command."""
        # Initialize source database
        init_args = mock.Mock()
        init_args.backend = 'sqlite'
        init_args.path = self.temp_db.name
        init_command(init_args)
        
        # Create a mock args object for migrate
        args = mock.Mock()
        args.from_backend = 'sqlite'
        args.to_backend = 'sqlite'
        args.from_path = self.temp_db.name
        args.to_path = self.target_db.name
        args.from_serializer = None
        args.to_serializer = None
        
        # Run the command
        result = migrate_command(args)
        self.assertEqual(result, 0)
        self.assertTrue(os.path.exists(self.target_db.name))
    
    def test_healthcheck_command(self):
        """Test the healthcheck command."""
        # Initialize database
        init_args = mock.Mock()
        init_args.backend = 'sqlite'
        init_args.path = self.temp_db.name
        init_command(init_args)
        
        # Create a mock args object
        args = mock.Mock()
        args.backend = 'sqlite'
        args.path = self.temp_db.name
        
        # Run the command
        result = healthcheck_command(args)
        self.assertEqual(result, 0)
    
    def test_list_command(self):
        """Test the list command."""
        # Initialize database
        init_args = mock.Mock()
        init_args.backend = 'sqlite'
        init_args.path = self.temp_db.name
        init_command(init_args)
        
        # Create a mock args object
        args = mock.Mock()
        args.backend = 'sqlite'
        args.path = self.temp_db.name
        
        # Run the command
        with mock.patch('builtins.print') as mock_print:
            result = list_command(args)
            self.assertEqual(result, 0)
