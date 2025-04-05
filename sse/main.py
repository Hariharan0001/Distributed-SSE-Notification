import uuid

from app import create_app
from config import Config
from app import INSTANCE_ID, active_subscribers
import atexit
from app.api.redis_cli import RedisClient

app = create_app(Config)

redis_client = RedisClient.get_instance()

# INSTANCE_ID = str(uuid.uuid4())
# active_subscribers = set()


@atexit.register
def shutdown():
    """Cleanup on server shutdown"""
    # keys = redis_client.keys('sse_connections:*')
    # for key in keys:
    #     print(key)
    #     redis_client.delete(key)
    try:
        # Clean up connections specific to this instance
        instance_key = f'instance:{INSTANCE_ID}:sse_connections'
        connections = redis_client.smembers(instance_key)
        for conn in connections:
            redis_client.delete(f"heartbeat:{conn}")
        redis_client.delete(instance_key)

        print(f"Cleaned up connections for instance {INSTANCE_ID}")
    except Exception as e:
        print(f"Error during shutdown cleanup for instance {INSTANCE_ID}: {e}")


if __name__ == "__main__":
    app.run(port=5001)
