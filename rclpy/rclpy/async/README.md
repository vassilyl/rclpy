# AsyncExecutor

The AsyncExecutor provides an async/await compatible executor for rclpy using [anyio](https://anyio.readthedocs.io/).

## Installation

AsyncExecutor requires the `anyio` package:

```bash
pip install anyio
```

## Usage

Since `async` is a reserved keyword in Python, you need to use `importlib` to import the module:

```python
import importlib
import anyio
import rclpy

# Import AsyncExecutor from 'async' module
rclpy_async = importlib.import_module('rclpy.async')
AsyncExecutor = rclpy_async.AsyncExecutor

async def main():
    ctx = rclpy.Context()
    rclpy.init(context=ctx)
    node = rclpy.create_node('my_node', context=ctx)
    
    def timer_callback():
        print("Timer callback!")
    
    timer = node.create_timer(1.0, timer_callback)
    
    try:
        async with AsyncExecutor(context=ctx) as executor:
            executor.add_node(node)
            # Run for 5 seconds
            await anyio.sleep(5)
    finally:
        node.destroy_timer(timer)
        node.destroy_node()
        rclpy.shutdown(context=ctx)

if __name__ == '__main__':
    anyio.run(main)
```

## Async Callbacks

AsyncExecutor supports both synchronous and asynchronous callbacks:

```python
import importlib
import anyio
import rclpy

rclpy_async = importlib.import_module('rclpy.async')
AsyncExecutor = rclpy_async.AsyncExecutor

async def main():
    ctx = rclpy.Context()
    rclpy.init(context=ctx)
    node = rclpy.create_node('async_node', context=ctx)
    
    # Async callback
    async def async_timer_callback():
        await anyio.sleep(0.1)
        print("Async timer callback!")
    
    # Regular callback
    def sync_timer_callback():
        print("Sync timer callback!")
    
    async_timer = node.create_timer(1.0, async_timer_callback)
    sync_timer = node.create_timer(2.0, sync_timer_callback)
    
    try:
        async with AsyncExecutor(context=ctx) as executor:
            executor.add_node(node)
            await anyio.sleep(5)
    finally:
        node.destroy_timer(async_timer)
        node.destroy_timer(sync_timer)
        node.destroy_node()
        rclpy.shutdown(context=ctx)

if __name__ == '__main__':
    anyio.run(main)
```

## Key Differences from Standard Executors

1. **Async Context Manager**: Use `async with AsyncExecutor()` instead of regular context manager
2. **Anyio Integration**: All callbacks run in an anyio task group
3. **Background Thread**: The wait loop runs in a background thread, allowing the main async context to do other work
4. **Import Method**: Must use `importlib.import_module('rclpy.async')` due to Python keyword restrictions

## Architecture

- **Main async context**: Your application's async code runs here
- **Background thread**: Runs the ROS 2 wait loop, detecting when callbacks are ready
- **Task group**: All callbacks are dispatched to an anyio task group for concurrent execution

This design allows you to mix ROS 2 callbacks with other async operations in a natural way.
