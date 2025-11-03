# AsyncExecutor class is a re-implementation of executors.SingleThreadedExecutor
# with the intention of running all async callbacks in an anyio task group.
# Instead of traditional boilerplate:
#
#    ctx = rclpy.Context()
#    rclpy.init(context=ctx)
#    node = rclpy.create_node('my_node', context=ctx)
#    # ... add node servers, clients, subscribers etc.
#    executor = rclpy.executors.SingleThreadedExecutor()
#    executor.add_node(node)
#    executor.spin()
#    rclpy.shutdown(context=ctx)
#
# With the AsyncExecutor, the equivalent code becomes:
#
#    ctx = rclpy.Context()
#    rclpy.init(context=ctx)
#    node = rclpy.create_node('my_node', context=ctx)
#    # ... add node servers, clients, subscribers etc.
#    async with AsyncExecutor() as executor:
#        executor.add_node(node)
#        anyio.sleep_forever()
#
# On entering the async context, AsyncExecutor creates anyio task group
# and spawns its own implementation of wait spinning loop in a worker thread.
# The loop just dispatches all callbacks to the task group for execution.
#
# The class doesn't inherit from rclpy.executors.Executor, but should be able
# to handle standard nodes and awaitables.
