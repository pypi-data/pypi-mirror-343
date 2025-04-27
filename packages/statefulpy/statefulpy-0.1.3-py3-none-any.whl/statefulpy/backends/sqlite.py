"""
SQLite backend for statefulpy.
"""
import os
import json
import sqlite3
import logging
import time
import threading
from typing import Any, Dict, Optional, Union
from sqlite3 import Connection

import portalocker

from .base import StateBackend
from statefulpy.serializers import get_serializer

logger = logging.getLogger(__name__)

# SQLite connection pool - thread-local connections
_local = threading.local()

# Add type annotations for file-lock tracking
_locks: Dict[str, Any] = {}
_lock_counts: Dict[str, int] = {}

class SQLiteBackend(StateBackend):
    """SQLite backend for state persistence."""

    def __init__(self, db_path: str = "stateful.db", serializer: str = "pickle"):
        """
        Initialize the SQLite backend.
        
        Args:
            db_path: Path to the SQLite database file
            serializer: Serializer to use ('pickle' or 'json')
        """
        super().__init__()
        self.db_path = db_path
        self.serializer = get_serializer(serializer)
        self._locks = {}
        self._lock_counts = {}  # For reentrance tracking
        
        # Create database directory if it doesn't exist
        db_dir = os.path.dirname(os.path.abspath(db_path))
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            
        # Initialize database
        self._init_db()
    
    def _get_connection(self) -> Connection:
        """Get a thread-local connection to the database."""
        if not hasattr(_local, 'conn') or _local.conn is None:
            _local.conn = sqlite3.connect(self.db_path)
            
            # Enable WAL journal mode for better concurrency
            _local.conn.execute("PRAGMA journal_mode=WAL;")
            
            # Set foreign keys constraint
            _local.conn.execute("PRAGMA foreign_keys=ON;")
            
            # Enable extended error codes
            _local.conn.execute("PRAGMA legacy_file_format=OFF;")
        
        return _local.conn

    def _init_db(self) -> None:
        """Initialize the database schema."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Create state table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS stateful_state (
                fn_id TEXT PRIMARY KEY,
                state BLOB,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            
            # Create lock table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS stateful_locks (
                fn_id TEXT PRIMARY KEY,
                locked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error initializing database: {e}")
            conn.rollback()
            raise
    
    def load_state(self, fn_id: str) -> Optional[Dict[str, Any]]:
        """
        Load state for a function from the database.
        
        Args:
            fn_id: Function identifier
            
        Returns:
            The state dictionary or None if it doesn't exist
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT state FROM stateful_state WHERE fn_id = ?",
                (fn_id,)
            )
            row = cursor.fetchone()
            
            if not row:
                return None
            
            state_data = row[0]
            return self.serializer.deserialize(state_data)
        except sqlite3.Error as e:
            logger.error(f"Error loading state for {fn_id}: {e}")
            return None
    
    def save_state(self, fn_id: str, state: Dict[str, Any]) -> bool:
        """
        Save state for a function to the database.
        
        Args:
            fn_id: Function identifier
            state: The state dictionary to save
            
        Returns:
            True if successful, False otherwise
        """
        if not state:
            return True  # Nothing to save
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            state_data = self.serializer.serialize(state)
            
            cursor.execute(
                """
                INSERT INTO stateful_state (fn_id, state) 
                VALUES (?, ?) 
                ON CONFLICT(fn_id) DO UPDATE SET 
                    state = excluded.state,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (fn_id, state_data)
            )
            
            conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error saving state for {fn_id}: {e}")
            conn.rollback()
            return False
    
    def acquire_lock(self, fn_id: str, timeout: float = 10.0) -> bool:
        """
        Acquire a lock for a function.
        
        Args:
            fn_id: Function identifier
            timeout: Timeout for acquiring the lock
            
        Returns:
            True if the lock was acquired, False otherwise
        """
        # Validate and convert db_path to an absolute path
        if not os.path.isabs(self.db_path):
            self.db_path = os.path.abspath(self.db_path)
            logger.warning(f"Converted db_path to absolute: {self.db_path}")

        # Check for reentrance - if we already hold the lock, just increment count
        if fn_id in self._locks and threading.current_thread().ident == self._locks[fn_id]:
            self._lock_counts[fn_id] += 1
            return True

        lock_file = f"{self.db_path}.{fn_id}.lock"
        try:
            if not os.path.exists(lock_file):
                open(lock_file, 'w').close()
            lock = portalocker.Lock(lock_file, timeout=timeout)
            lock.acquire()
            self._locks[fn_id] = threading.current_thread().ident
            self._lock_counts[fn_id] = 1
            
            # Also insert into the database for visibility
            conn = self._get_connection()
            cursor = conn.cursor()
            
            try:
                cursor.execute(
                    """
                    INSERT INTO stateful_locks (fn_id) 
                    VALUES (?) 
                    ON CONFLICT(fn_id) DO UPDATE SET 
                        locked_at = CURRENT_TIMESTAMP
                    """,
                    (fn_id,)
                )
                conn.commit()
            except sqlite3.Error as e:
                logger.error(f"Error updating lock table for {fn_id}: {e}")
                # Continue anyway - the file lock is the real lock
            
            return True
        except (portalocker.LockException, IOError) as e:
            logger.error(f"Error acquiring lock for {fn_id}: {e}")
            return False
    
    def release_lock(self, fn_id: str) -> bool:
        """
        Release a lock for a function.
        
        Args:
            fn_id: Function identifier
            
        Returns:
            True if the lock was released, False otherwise
        """
        # Check if we hold the lock
        if fn_id not in self._locks or threading.current_thread().ident != self._locks[fn_id]:
            return False
        
        # Decrease lock count for reentrant locks
        self._lock_counts[fn_id] -= 1
        
        # If we still have active locks, don't release yet
        if self._lock_counts[fn_id] > 0:
            return True
        
        lock_file = f"{self.db_path}.{fn_id}.lock"
        retries = 3
        for attempt in range(retries):
            try:
                # Attempt to release the file lock
                lock = portalocker.Lock(lock_file)
                lock.release()
                # Try to remove the lock file
                if os.path.exists(lock_file):
                    os.unlink(lock_file)
                break
            except (portalocker.LockException, IOError) as e:
                logger.error(f"Attempt {attempt+1} – Error releasing lock for {fn_id}: {e}")
                time.sleep(0.5)
        else:
            logger.error(f"Failed to release lock for {fn_id} after {retries} attempts")
            return False

        # Remove from our tracking
        del self._locks[fn_id]
        del self._lock_counts[fn_id]
        
        # Remove from the database too
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "DELETE FROM stateful_locks WHERE fn_id = ?",
                (fn_id,)
            )
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error cleaning up lock table for {fn_id}: {e}")
            # Continue anyway - the file lock is the real lock
        
        return True
    
    def close(self) -> None:
        """Close the database connection."""
        if hasattr(_local, 'conn') and _local.conn:
            try:
                _local.conn.close()
                _local.conn = None
            except sqlite3.Error as e:
                logger.error(f"Error closing SQLite connection: {e}")
