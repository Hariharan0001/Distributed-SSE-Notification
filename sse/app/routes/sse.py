import json
import queue
import threading
import time
from flask import request, stream_with_context, Response, jsonify
from flask_restx import Resource
from ipss_utils.decorators import login_required

from ..api_doc import sse_api_route
from ..api.redis_cli import RedisClient
from ..api.decorator import require_valid_uuid
from ..api.SSEConnectionFactory import SSEConnectionFactory
from ..api.NotificationSubscriber import NotificationSubscriber
from ..api.NotificationPublisher import NotificationPublisher
from ..api_doc import send_message_model


@sse_api_route.route('/uuid')
class CreateID(Resource):

    @login_required()
    def get(self):
        """
        Get the unique_id for each session user
        :return:
        """
        user_id = request.args.get('current_user',{}).get('userid', None)
        redis_cli = RedisClient()
        uuid_val = SSEConnectionFactory.create_connection()

        redis_cli.setex(str(uuid_val), 30, user_id)

        return jsonify({
            'uuid': str(uuid_val)
        })


@sse_api_route.route('/sse')
class SSE(Resource):

    @require_valid_uuid
    def get(self):
        """
        Establish an SSE Connection
        """
        # user_id = request.args.get('user_id')
        # redis_cli = RedisClient()
        #
        # connection_id = SSEConnectionFactory.create_connection()  # Unique connection ID
        #
        # subscriber_obj = NotificationSubscriber(user_id=user_id, redis_client=redis_cli, connection_id=connection_id)
        #
        # def event_stream():
        #     try:
        #         while True:
        #             message = subscriber_obj.message_queue.get()  # Get message from queue
        #             print(message)
        #             yield f"data: {json.dumps(message)}\n\n"
        #     except GeneratorExit:
        #         print(f"Client {subscriber_obj.user_id} uuid-{subscriber_obj.connection_id} disconnected")
        #         subscriber_obj.cleanup()
        #
        # # Add connection ID to Redis
        # subscriber_obj.add_sse_connection()
        #
        # # Start Redis pubsub listener in background thread
        # threading.Thread(target=subscriber_obj.listen, daemon=True).start()
        #
        # return Response(stream_with_context(event_stream()), content_type='text/event-stream')
        user_id = request.args.get('user_id')
        redis_cli = RedisClient()
        connection_id = SSEConnectionFactory.create_connection()

        subscriber = NotificationSubscriber(redis_client=redis_cli,
                                            user_id=user_id,
                                            connection_id=connection_id)

        def event_stream():
            try:
                while True:
                    message = subscriber.message_queue.get()
                    yield f"data: {json.dumps(message)}\n\n"
            except GeneratorExit:
                print("remove")
                subscriber.cleanup()

        subscriber.add_sse_connection()
        threading.Thread(target=subscriber.listen, daemon=True).start()
        return Response(stream_with_context(event_stream()),
                        content_type='text/event-stream')


@sse_api_route.route('/send_message')
class SendNotification(Resource):

    @login_required()
    @sse_api_route.expect(send_message_model)
    def post(self):
        """
        Send Notification
        """
        data = request.json
        user_ids = data.get('user_ids', [])
        message = data.get('message', '')
        NotificationPublisher.send_notifications(user_ids=user_ids, message=message)
        return {
            'message': 'message send successfully'
        }




