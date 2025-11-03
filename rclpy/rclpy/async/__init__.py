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

"""
Async support for rclpy.

Note: 'async' is a reserved keyword in Python. To import from this module:
    
    # Method 1: Import using importlib
    import importlib
    async_module = importlib.import_module('rclpy.async')
    AsyncExecutor = async_module.AsyncExecutor
    
    # Method 2: Use __import__
    rclpy_async = __import__('rclpy.async', fromlist=['AsyncExecutor'])
    AsyncExecutor = rclpy_async.AsyncExecutor
"""

# Import at module level for proper initialization
# This file can be imported using importlib or __import__
from .executor import AsyncExecutor  # noqa: F401

__all__ = ['AsyncExecutor']
