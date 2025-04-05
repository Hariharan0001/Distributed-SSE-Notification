from functools import wraps

from flask import request
from ..api.redis_cli import RedisClient


def is_valid_uuid(user_id, client_uuid, redis_cli):
    if user_id != redis_cli.get(client_uuid):
        return False
    redis_cli.delete(client_uuid)
    return True


def require_valid_uuid(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = request.args.get('user_id')
        client_uuid = request.args.get('uuid')
        redis_cli = RedisClient()

        if not user_id or not client_uuid or not is_valid_uuid(user_id, client_uuid, redis_cli):
            return {"error": "Invalid or expired UUID"}, 403
        return func(*args, **kwargs)

    return wrapper
