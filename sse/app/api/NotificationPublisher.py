import json
import time
import uuid

from .redis_cli import RedisClient


class NotificationPublisher:

    @staticmethod
    def send_notifications(user_ids, message, channel=None):
        """Publish a message to multiple user channels"""
        redis_cli = RedisClient()

        # for user_id in user_ids:
        #     if not channel:
        #         channel = f'product_alert_{user_id}'
        #     print('print channel from Notification Publisher', channel)
        #     redis_cli.publish(channel, json.dumps(message))
        #     print(f"Notification sent to {user_id}: {message}")

        message_data = {
            'message_id': str(uuid.uuid4()),
            'content': message,
            'timestamp': time.time()
        }

        for user_id in user_ids:
            channel_name = f'product_alert_{user_id}'
            redis_cli.publish(channel_name, json.dumps(message_data))
