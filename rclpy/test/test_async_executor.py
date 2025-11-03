# Copyright 2024 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import importlib
import time
import unittest

import rclpy

# Import AsyncExecutor from 'async' module (reserved keyword requires importlib)
rclpy_async = importlib.import_module('rclpy.async')
AsyncExecutor = rclpy_async.AsyncExecutor

try:
    import anyio
    HAS_ANYIO = True
except ImportError:
    HAS_ANYIO = False


@unittest.skipUnless(HAS_ANYIO, 'anyio not available')
class TestAsyncExecutor(unittest.TestCase):

    def setUp(self) -> None:
        self.context = rclpy.context.Context()
        rclpy.init(context=self.context)
        self.node = rclpy.create_node(
            'TestAsyncExecutor',
            namespace='/rclpy',
            context=self.context
        )

    def tearDown(self) -> None:
        self.node.destroy_node()
        rclpy.shutdown(context=self.context)
        self.context.destroy()

    def test_async_executor_creation(self) -> None:
        """Test that AsyncExecutor can be created."""
        executor = AsyncExecutor(context=self.context)
        self.assertIsNotNone(executor)
        executor.shutdown()

    def test_async_executor_add_node(self) -> None:
        """Test adding a node to AsyncExecutor."""
        executor = AsyncExecutor(context=self.context)
        self.assertTrue(executor.add_node(self.node))
        self.assertEqual(len(executor.get_nodes()), 1)
        executor.shutdown()

    def test_async_executor_remove_node(self) -> None:
        """Test removing a node from AsyncExecutor."""
        executor = AsyncExecutor(context=self.context)
        executor.add_node(self.node)
        executor.remove_node(self.node)
        self.assertEqual(len(executor.get_nodes()), 0)
        executor.shutdown()

    def test_async_executor_context_manager(self) -> None:
        """Test AsyncExecutor as async context manager."""
        async def test_context() -> None:
            async with AsyncExecutor(context=self.context) as executor:
                self.assertIsNotNone(executor)
                executor.add_node(self.node)
                self.assertEqual(len(executor.get_nodes()), 1)
                # Sleep briefly to allow spin thread to run
                await anyio.sleep(0.1)

        anyio.run(test_context)

    def test_async_executor_timer_callback(self) -> None:
        """Test that timer callbacks are executed."""
        callback_called = []

        def timer_callback() -> None:
            callback_called.append(True)

        async def test_timer() -> None:
            async with AsyncExecutor(context=self.context) as executor:
                tmr = self.node.create_timer(0.01, timer_callback)
                executor.add_node(self.node)
                
                # Wait for callback to be called
                for _ in range(50):
                    await anyio.sleep(0.1)
                    if callback_called:
                        break
                
                self.node.destroy_timer(tmr)

        anyio.run(test_timer)
        self.assertTrue(len(callback_called) > 0)

    def test_async_executor_async_callback(self) -> None:
        """Test that async callbacks are executed."""
        callback_called = []

        async def async_timer_callback() -> None:
            await anyio.sleep(0.01)
            callback_called.append(True)

        async def test_async_timer() -> None:
            async with AsyncExecutor(context=self.context) as executor:
                tmr = self.node.create_timer(0.01, async_timer_callback)
                executor.add_node(self.node)
                
                # Wait for callback to be called
                for _ in range(50):
                    await anyio.sleep(0.1)
                    if callback_called:
                        break
                
                self.node.destroy_timer(tmr)

        anyio.run(test_async_timer)
        self.assertTrue(len(callback_called) > 0)


if __name__ == '__main__':
    unittest.main()
