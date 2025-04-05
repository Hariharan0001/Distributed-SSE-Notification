from flask_restx import Namespace, fields


sse_api_route = Namespace('SSE Api Route', path='/sse')


notification_post_field = {
    'user_ids': fields.List(fields.Integer),
    'message': fields.String
}

send_message_model = sse_api_route.model('send message model', notification_post_field)
