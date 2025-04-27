"""
Command-line interface for StatefulPy.
"""
import argparse
import sys
import logging
import os
import json
import time
import pickle

from statefulpy.backends.base import get_backend
from statefulpy.config import get_backend_options

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def init_command(args):
    """Initialize a backend storage."""
    backend_type = args.backend
    options = get_backend_options(backend_type)
    
    if backend_type == 'sqlite':
        db_path = args.path or options.get('db_path', 'statefulpy.db')
        options['db_path'] = db_path
        
        # Create directory if it doesn't exist
        dir_path = os.path.dirname(os.path.abspath(db_path))
        if dir_path and not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
                logger.info(f"Created directory {dir_path}")
            except OSError as e:
                logger.error(f"Failed to create directory {dir_path}: {e}")
                return 1
        
        logger.info(f"Initializing SQLite backend at {db_path}")
    
    elif backend_type == 'redis':
        redis_url = args.path or options.get('redis_url', 'redis://localhost:6379/0')
        options['redis_url'] = redis_url
        logger.info(f"Initializing Redis backend at {redis_url}")
    
    try:
        backend = get_backend(backend_type, **options)
        
        # For SQLite, the _setup_database method creates the schema
        if backend_type == 'sqlite':
            # The backend was already initialized in the constructor
            pass
        
        # Test connection
        test_key = "statefulpy:init:test"
        test_data = {"initialized": True, "timestamp": time.time()}
        
        if not backend.save_state(test_key, test_data):
            logger.error(f"Failed to write to {backend_type} backend")
            return 1
            
        loaded_data = backend.load_state(test_key)
        if not loaded_data:
            logger.error(f"Failed to read from {backend_type} backend")
            return 1
            
        logger.info(f"Successfully initialized {backend_type} backend")
        return 0
    except Exception as e:
        logger.error(f"Failed to initialize {backend_type} backend: {e}")
        return 1


def migrate_command(args):
    """Migrate state from one backend to another."""
    source_type = args.from_backend
    target_type = args.to_backend
    
    source_options = get_backend_options(source_type)
    target_options = get_backend_options(target_type)
    
    # Handle source options
    if args.from_path:
        if source_type == 'sqlite':
            source_options['db_path'] = args.from_path
        elif source_type == 'redis':
            source_options['redis_url'] = args.from_path
    
    # Handle target options
    if args.to_path:
        if target_type == 'sqlite':
            target_options['db_path'] = args.to_path
        elif target_type == 'redis':
            target_options['redis_url'] = args.to_path
    
    # Process optional serializer arguments
    if args.from_serializer:
        source_options['serializer'] = args.from_serializer
    if args.to_serializer:
        target_options['serializer'] = args.to_serializer
    
    logger.info(f"Migrating from {source_type} to {target_type}")
    
    # Validate paths exist for sqlite
    if source_type == 'sqlite' and not os.path.exists(source_options['db_path']):
        logger.error(f"Source database not found: {source_options['db_path']}")
        return 1
    
    # Create target directory if needed
    if target_type == 'sqlite':
        target_dir = os.path.dirname(os.path.abspath(target_options['db_path']))
        if target_dir and not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir, exist_ok=True)
            except OSError as e:
                logger.error(f"Failed to create target directory {target_dir}: {e}")
                return 1
    
    try:
        source_backend = get_backend(source_type, **source_options)
        target_backend = get_backend(target_type, **target_options)
        
        # Handle migration based on backends
        if source_type == 'sqlite':
            try:
                # Use a context manager for the connection
                with source_backend._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT fn_id, state FROM stateful_state")
                    records = cursor.fetchall()
                    
                    if not records:
                        logger.info("No state records found to migrate")
                        return 0
                        
                    logger.info(f"Found {len(records)} state records to migrate")
                    migrated_count = 0
                    
                    for fn_id, state_blob in records:
                        try:
                            # Deserialize based on source backend's serializer
                            if source_backend.serializer == "pickle":
                                state = pickle.loads(state_blob)
                            else:  # json
                                state = json.loads(state_blob.decode('utf-8'))
                            
                            # Save to target backend
                            if target_backend.save_state(fn_id, state):
                                logger.debug(f"Migrated state for {fn_id}")
                                migrated_count += 1
                            else:
                                logger.error(f"Failed to migrate state for {fn_id}")
                                
                        except Exception as e:
                            logger.error(f"Error migrating state for {fn_id}: {e}")
                    
                    logger.info(f"Successfully migrated {migrated_count}/{len(records)} records")
            
            except Exception as e:
                logger.error(f"SQLite migration error: {e}")
                return 1
        
        # For Redis, we need to scan for keys with our prefix
        elif source_type == 'redis':
            prefix = source_options.get('prefix', 'statefulpy:')
            state_prefix = f"{prefix}state:"
            
            # Scan for keys matching our pattern
            cursor = 0
            all_keys = []
            
            try:
                while True:
                    cursor, keys = source_backend.client.scan(
                        cursor=cursor, 
                        match=f"{state_prefix}*", 
                        count=100
                    )
                    all_keys.extend(keys)
                    if cursor == 0:
                        break
                
                if not all_keys:
                    logger.info("No state records found to migrate")
                    return 0
                
                logger.info(f"Found {len(all_keys)} state records to migrate")
                migrated_count = 0
                
                # Process each key
                for key in all_keys:
                    try:
                        # Extract function ID from key
                        fn_id = key.decode('utf-8').replace(state_prefix, '')
                        
                        # Get state data
                        state_data = source_backend.load_state(fn_id)
                        
                        if state_data:
                            # Save to target backend
                            if target_backend.save_state(fn_id, state_data):
                                logger.debug(f"Migrated state for {fn_id}")
                                migrated_count += 1
                            else:
                                logger.error(f"Failed to migrate state for {fn_id}")
                    except Exception as e:
                        logger.error(f"Error migrating state for key {key}: {e}")
                
                logger.info(f"Successfully migrated {migrated_count}/{len(all_keys)} records")
                
            except Exception as e:
                logger.error(f"Redis migration error: {e}")
                return 1
        
        logger.info(f"Successfully migrated state from {source_type} to {target_type}")
        return 0
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return 1


def healthcheck_command(args):
    """Check the health of a backend."""
    backend_type = args.backend
    options = get_backend_options(backend_type)
    
    if args.path:
        if backend_type == 'sqlite':
            options['db_path'] = args.path
        elif backend_type == 'redis':
            options['redis_url'] = args.path
    
    try:
        backend = get_backend(backend_type, **options)
        
        # Use a test key that's safe for all filesystems (avoid special chars)
        test_key = f"statefulpy_healthcheck_{int(time.time())}"
        test_data = {"timestamp": time.time(), "healthy": True}
        
        logger.info(f"Testing {backend_type} backend write operation")
        if not backend.save_state(test_key, test_data):
            logger.error(f"Failed to write to {backend_type} backend")
            return 1
        
        logger.info(f"Testing {backend_type} backend read operation")
        read_data = backend.load_state(test_key)
        if not read_data:
            logger.error(f"Failed to read from {backend_type} backend")
            return 1
        
        # Test lock acquisition
        logger.info(f"Testing {backend_type} backend lock acquisition")
        if not backend.acquire_lock(test_key):
            logger.error(f"Failed to acquire lock on {backend_type} backend")
            return 1
        
        # Test lock release
        logger.info(f"Testing {backend_type} backend lock release")
        if not backend.release_lock(test_key):
            logger.error(f"Failed to release lock on {backend_type} backend")
            return 1
        
        logger.info(f"{backend_type.capitalize()} backend health check passed!")
        return 0
    except Exception as e:
        logger.error(f"Health check for {backend_type} backend failed: {e}")
        return 1


def list_command(args):
    """List all stateful functions in a backend."""
    backend_type = args.backend
    options = get_backend_options(backend_type)
    
    if args.path:
        if backend_type == 'sqlite':
            options['db_path'] = args.path
        elif backend_type == 'redis':
            options['redis_url'] = args.path
    
    try:
        backend = get_backend(backend_type, **options)
        
        if backend_type == 'sqlite':
            try:
                with backend._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT fn_id, updated_at FROM stateful_state ORDER BY updated_at DESC")
                    records = cursor.fetchall()
                    
                    if not records:
                        print("No stateful functions found in the database.")
                        return 0
                    
                    print(f"\nFound {len(records)} stateful functions:")
                    print(f"{'FUNCTION ID':<50} {'LAST UPDATED':<20}")
                    print("-" * 70)
                    
                    for fn_id, updated_at in records:
                        print(f"{fn_id:<50} {updated_at:<20}")
                    
                    return 0
            except Exception as e:
                logger.error(f"Failed to list SQLite functions: {e}")
                return 1
        elif backend_type == 'redis':
            try:
                prefix = options.get('prefix', 'statefulpy:')
                state_prefix = f"{prefix}state:"
                
                # Scan for keys matching our pattern
                cursor = 0
                all_keys = []
                
                while True:
                    cursor, keys = backend.client.scan(
                        cursor=cursor, 
                        match=f"{state_prefix}*", 
                        count=100
                    )
                    all_keys.extend(keys)
                    if cursor == 0:
                        break
                
                if not all_keys:
                    print("No stateful functions found in Redis.")
                    return 0
                
                # Extract function IDs from keys
                function_ids = [key.decode('utf-8').replace(state_prefix, '') for key in all_keys]
                
                print(f"\nFound {len(function_ids)} stateful functions:")
                print(f"{'FUNCTION ID':<50}")
                print("-" * 50)
                
                for fn_id in sorted(function_ids):
                    print(f"{fn_id:<50}")
                
                return 0
            except Exception as e:
                logger.error(f"Failed to list Redis functions: {e}")
                return 1
    except Exception as e:
        logger.error(f"Failed to connect to {backend_type} backend: {e}")
        return 1


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="StatefulPy CLI - Manage persistent function state"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # init command
    init_parser = subparsers.add_parser("init", help="Initialize storage for state persistence")
    init_parser.add_argument(
        "--backend", 
        choices=["sqlite", "redis"], 
        default="sqlite",
        help="Backend type to initialize (default: sqlite)"
    )
    init_parser.add_argument(
        "--path", 
        help="Path to database file (SQLite) or Redis URL"
    )
    
    # migrate command
    migrate_parser = subparsers.add_parser("migrate", help="Migrate state between backends")
    migrate_parser.add_argument(
        "--from", 
        dest="from_backend",
        choices=["sqlite", "redis"], 
        default="sqlite",
        help="Source backend type (default: sqlite)"
    )
    migrate_parser.add_argument(
        "--to", 
        dest="to_backend",
        choices=["sqlite", "redis"], 
        default="redis",
        help="Target backend type (default: redis)"
    )
    migrate_parser.add_argument(
        "--from-path", 
        help="Path to source database file (SQLite) or Redis URL"
    )
    migrate_parser.add_argument(
        "--to-path", 
        help="Path to target database file (SQLite) or Redis URL"
    )
    migrate_parser.add_argument(
        "--from-serializer",
        choices=["pickle", "json"],
        help="Source serializer type"
    )
    migrate_parser.add_argument(
        "--to-serializer",
        choices=["pickle", "json"],
        help="Target serializer type"
    )
    
    # healthcheck command
    healthcheck_parser = subparsers.add_parser("healthcheck", help="Check the health of a backend")
    healthcheck_parser.add_argument(
        "--backend", 
        choices=["sqlite", "redis"], 
        default="sqlite",
        help="Backend type to check (default: sqlite)"
    )
    healthcheck_parser.add_argument(
        "--path", 
        help="Path to database file (SQLite) or Redis URL"
    )
    
    # list command
    list_parser = subparsers.add_parser("list", help="List all stateful functions in a backend")
    list_parser.add_argument(
        "--backend", 
        choices=["sqlite", "redis"], 
        default="sqlite",
        help="Backend type to list from (default: sqlite)"
    )
    list_parser.add_argument(
        "--path", 
        help="Path to database file (SQLite) or Redis URL"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    if args.command == "init":
        return init_command(args)
    elif args.command == "migrate":
        return migrate_command(args)
    elif args.command == "healthcheck":
        return healthcheck_command(args)
    elif args.command == "list":
        return list_command(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
