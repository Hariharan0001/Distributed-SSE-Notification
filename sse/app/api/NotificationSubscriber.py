# import queue
#
# from flask import json
#
#
# class NotificationSubscriber:
#     """Handles listening to Redis channels for notifications."""
#
#     def __init__(self, redis_client, user_id, connection_id):
#         self.redis_client = redis_client
#         self.user_id = user_id
#         self.connection_id = connection_id
#         self.pubsub = self.redis_client.pubsub()
#         self.active_sse_connections = {}
#         self.message_queue = queue.Queue()
#         self.redis_cli_key = f'sse_connections:{self.user_id}'
#
#     def add_sse_connection(self):
#         self.redis_client.sadd(self.redis_cli_key, self.connection_id)
#         print(f"SSE connection added for {self.user_id}.")
#
#     def remove_sse_connection(self):
#         self.redis_client.srem(self.redis_cli_key, self.connection_id)
#         print("connection Removed")
#
#     def cleanup(self):
#         self.pubsub.unsubscribe(f'product_alert_{self.user_id}')
#         self.remove_sse_connection()
#         self.pubsub.close()
#
#     def listen(self):
#         """Listen for messages on the Redis pubsub channel"""
#         channel_name = f'product_alert_{self.user_id}'
#         self.pubsub.subscribe(channel_name)
#         print(f"Listening on {channel_name} for {self.user_id}")
#
#         try:
#             for message in self.pubsub.listen():
#                 if message['type'] == 'message':
#                     data = json.loads(message['data'])
#                     print(f"Received alert for {self.user_id} {self.connection_id}: {data}")
#
#                     # Get all active connections for the user from Redis
#                     connection_ids = self.redis_client.smembers(self.redis_cli_key)
#
#                     for connection_id in connection_ids:
#                         sse_conn = self.active_sse_connections.get(connection_id)
#                         if sse_conn:
#                             try:
#                                 sse_conn['queue'].put(data)  # Use queue to send data
#                             except Exception as e:
#                                 print(f"Error sending to {self.user_id}: {e}")
#                                 self.cleanup()
#         except Exception as e:
#             print(f"Error in pubsub for {self.user_id}: {e}")
#             self.cleanup()
#


# api/notification_subscriber.py
import queue
import json
import threading
import time
import uuid
from threading import Thread

#
# class NotificationSubscriber:
#
#     def __init__(self, redis_client, user_id, connection_id):
#         self.redis_client = redis_client
#         self.user_id = user_id
#         self.connection_id = connection_id
#         self.pubsub = self.redis_client.pubsub()
#         self.active_sse_connections = {}  # Local cache of connections
#         self.message_queue = queue.Queue()
#         self.redis_cli_key = f'sse_connections:{self.user_id}'
#         self.processed_messages = set()  # For deduplication
#         self.running = True
#
#         # Start heartbeat mechanism
#         self._start_heartbeat()
#
#     def add_sse_connection(self):
#         """Add SSE connection to Redis and local cache"""
#         # Add to Redis set with TTL
#         self.redis_client.sadd(self.redis_cli_key, self.connection_id)
#         # Set heartbeat key with TTL (5 minutes)
#         self.redis_client.setex(f"heartbeat:{self.connection_id}", 300, time.time())
#         # Add to local cache
#         self.active_sse_connections[self.connection_id] = {
#             'queue': self.message_queue,
#             'last_active': time.time()
#         }
#         print(f"SSE connection added for {self.user_id}.")
#
#     def remove_sse_connection(self):
#         """Remove SSE connection from Redis and local cache"""
#         self.redis_client.srem(self.redis_cli_key, self.connection_id)
#         self.redis_client.delete(f"heartbeat:{self.connection_id}")
#         self.active_sse_connections.pop(self.connection_id, None)
#         print("connection Removed")
#
#     def cleanup(self):
#         """Clean up resources on disconnection"""
#         self.running = False
#         self.pubsub.unsubscribe(f'product_alert_{self.user_id}')
#         self.remove_sse_connection()
#         self.pubsub.close()
#
#     def _start_heartbeat(self):
#         """Start heartbeat mechanism to maintain connection health"""
#
#         def heartbeat_loop():
#             while self.running:
#                 self.redis_client.setex(f"heartbeat:{self.connection_id}", 300, time.time())
#                 time.sleep(30)  # Heartbeat every 30 seconds
#
#         threading.Thread(target=heartbeat_loop, daemon=True).start()
#
#     def listen(self):
#         """Listen for messages on the Redis pubsub channel"""
#         channel_name = f'product_alert_{self.user_id}'
#         self.pubsub.subscribe(channel_name)
#         print(f"Listening on {channel_name} for {self.user_id}")
#
#         try:
#             for message in self.pubsub.listen():
#                 if not self.running:
#                     break
#                 if message['type'] == 'message':
#                     data = json.loads(message['data'])
#                     message_id = data.get('message_id', str(uuid.uuid4()))  # Ensure unique message ID
#
#                     # Deduplication check
#                     if message_id in self.processed_messages:
#                         continue
#
#                     self.processed_messages.add(message_id)
#                     print(f"Received alert for {self.user_id} {self.connection_id}: {data}")
#
#                     # Get all active connections for the user from Redis
#                     connection_ids = self.redis_client.smembers(self.redis_cli_key)
#
#                     # Send to all active connections
#                     for conn_id in connection_ids:
#                         sse_conn = self.active_sse_connections.get(conn_id)
#                         if sse_conn:
#                             try:
#                                 sse_conn['queue'].put(data)  # Use queue to send data
#                                 sse_conn['last_active'] = time.time()
#                             except Exception as e:
#                                 print(f"Error sending to {self.user_id} connection {conn_id}: {e}")
#                                 self.active_sse_connections.pop(conn_id, None)
#                         else:
#                             # If connection not in local cache but in Redis, remove it
#                             if self.redis_client.get(f"heartbeat:{conn_id}") is None:
#                                 self.redis_client.srem(self.redis_cli_key, conn_id)
#
#                     # Maintain processed_messages size
#                     if len(self.processed_messages) > 1000:
#                         self.processed_messages = set(list(self.processed_messages)[-500:])
#
#         except Exception as e:
#             print(f"Error in pubsub for {self.user_id}: {e}")
#             self.cleanup()


# api/notification_subscriber.py
import queue
import json
import time
import threading
from uuid import uuid4
from app import INSTANCE_ID


class NotificationSubscriber:
    """Handles listening to Redis channels for notifications."""

    def __init__(self, redis_client, user_id, connection_id):
        self.redis_client = redis_client
        self.user_id = user_id
        self.connection_id = connection_id
        self.pubsub = self.redis_client.pubsub()
        self.active_sse_connections = {}
        self.message_queue = queue.Queue()
        self.instance_key = f'instance:{INSTANCE_ID}:sse_connections'
        self.redis_cli_key = f'sse_connections:{self.user_id}'  # Still track per-user for message delivery
        self.processed_messages = set()
        self.running = True
        self.heartbeat_thread = None

        # Add to global tracking
        from app import active_subscribers
        active_subscribers.add(self)

        self._start_heartbeat()

    def add_sse_connection(self):
        """Add SSE connection to Redis with instance-specific tracking"""
        # Track connection per instance
        self.redis_client.sadd(self.instance_key, self.connection_id)
        # Also track per user for message delivery
        self.redis_client.sadd(self.redis_cli_key, self.connection_id)
        self.redis_client.setex(f"heartbeat:{self.connection_id}", 300, time.time())
        self.active_sse_connections[self.connection_id] = {
            'queue': self.message_queue,
            'last_active': time.time()
        }
        print(f"SSE connection added for {self.user_id} on instance {INSTANCE_ID}.")

    def remove_sse_connection(self):
        """Remove SSE connection from Redis and local cache"""
        self.redis_client.srem(self.instance_key, self.connection_id)
        self.redis_client.srem(self.redis_cli_key, self.connection_id)
        self.redis_client.delete(f"heartbeat:{self.connection_id}")
        self.active_sse_connections.pop(self.connection_id, None)
        print("connection Removed")

    def cleanup(self):
        """Clean up resources on disconnection"""
        self.running = False
        if self.pubsub:
            self.pubsub.unsubscribe(f'product_alert_{self.user_id}')
            self.pubsub.close()
        self.remove_sse_connection()
        from app import active_subscribers
        active_subscribers.discard(self)

    def _start_heartbeat(self):
        """Start heartbeat mechanism to maintain connection health"""

        def heartbeat_loop():
            while self.running:
                try:
                    self.redis_client.setex(f"heartbeat:{self.connection_id}", 300, time.time())
                    time.sleep(30)
                except Exception as e:
                    print(f"Heartbeat error for {self.user_id}: {e}")
                    break

        self.heartbeat_thread = threading.Thread(target=heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()

    def listen(self):
        """Listen for messages on the Redis pubsub channel"""
        channel_name = f'product_alert_{self.user_id}'
        self.pubsub.subscribe(channel_name)
        print(f"Listening on {channel_name} for {self.user_id}")

        try:
            for message in self.pubsub.listen():
                if not self.running:
                    break
                if message['type'] == 'message':
                    data = json.loads(message['data'])
                    message_id = data.get('message_id', str(uuid4()))

                    if message_id in self.processed_messages:
                        continue

                    self.processed_messages.add(message_id)
                    print(f"Received alert for {self.user_id} {self.connection_id}: {data}")

                    connection_ids = self.redis_client.smembers(self.redis_cli_key)
                    for conn_id in connection_ids:
                        sse_conn = self.active_sse_connections.get(conn_id)
                        if sse_conn:
                            try:
                                sse_conn['queue'].put(data)
                                sse_conn['last_active'] = time.time()
                            except Exception as e:
                                print(f"Error sending to {self.user_id} connection {conn_id}: {e}")
                                self.active_sse_connections.pop(conn_id, None)
                        else:
                            if self.redis_client.get(f"heartbeat:{conn_id}") is None:
                                self.redis_client.srem(self.redis_cli_key, conn_id)
                                self.redis_client.srem(self.instance_key, conn_id)

                    if len(self.processed_messages) > 1000:
                        self.processed_messages = set(list(self.processed_messages)[-500:])

        except Exception as e:
            print(f"Error in pubsub for {self.user_id}: {e}")
            self.cleanup()
