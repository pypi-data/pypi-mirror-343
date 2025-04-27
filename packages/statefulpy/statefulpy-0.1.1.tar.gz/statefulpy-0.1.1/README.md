# StatefulPy

**StatefulPy** provides transparent, persistent state management for regular Python functions.

## Features

- **Simple Decorator API**: Add persistent state to any function with a decorator
- **Multiple Backends**: Store state in SQLite (embedded) or Redis (distributed)
- **Automatic State Management**: State is automatically loaded, saved, and synchronized
- **Concurrency Safe**: Locks ensure state consistency across threads and processes
- **Flexible Serialization**: Support for pickle, JSON, and custom serializers
- **CLI Tools**: Manage, migrate, and monitor your function state

## Installation

```bash
pip install statefulpy
```

For Redis support:

```bash
pip install statefulpy[redis]
```

**Security Warning:**  
The default serializer used by StatefulPy is **Pickle** for performance reasons.  
However, **Pickle is insecure** if processing untrusted input.  
For public-facing or untrusted data applications, use the JSON serializer instead:

```python
@stateful(backend="sqlite", db_path="state.db", serializer="json")
def my_function():
    # Your function code...
```

## Quickstart

```python
from statefulpy import stateful

@stateful(backend="sqlite", db_path="counter.db")
def counter():
    # Initialize state if needed
    if "count" not in counter.state:
        counter.state["count"] = 0
    
    # Update state
    counter.state["count"] += 1
    
    return counter.state["count"]

# The counter value persists across runs
print(counter())  # 1 (first run)
print(counter())  # 2
# Restart your program...
print(counter())  # 3 (value was loaded from storage)
```

## Backend Options

### SQLite (Default)

```python
@stateful(backend="sqlite", db_path="state.db", serializer="pickle")
def my_function():
    # Your function code...
```

### Redis

```python
@stateful(backend="redis", redis_url="redis://localhost:6379/0")
def my_function():
    # Your function code...
```

## Global Configuration

```python
from statefulpy import set_backend

# Set default backend for all @stateful functions
set_backend("redis", redis_url="redis://localhost:6379/0")
```

## Serialization

StatefulPy supports multiple serialization formats:

- **Using JSON serializer:**  
  For security, the recommended serializer for public-facing applications is JSON.

  ```python
  @stateful(backend="sqlite", db_path="state.db", serializer="json")
  def my_function():
      # Your function code...
  ```

- **Using the Pickle serializer:**  
  Pickle offers better performance but is insecure against untrusted input.

  ⚠️ **Warning:** Only use Pickle when handling trusted data.

  ```python
  @stateful(backend="sqlite", db_path="state.db", serializer="pickle")
  def my_function():
      # Your function code...
  ```

## Command-Line Interface

**Initialize storage:**

```bash
statefulpy init --backend sqlite --path state.db
```

**Migrate between backends:**

```bash
statefulpy migrate --from sqlite --to redis --from-path state.db --to-path redis://localhost:6379/0
```

**Check backend health:**

```bash
statefulpy healthcheck --backend redis --path redis://localhost:6379/0
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
