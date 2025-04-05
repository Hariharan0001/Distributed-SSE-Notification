import uuid


class SSEConnectionFactory:
    """Creates and manages SSE connections."""

    @staticmethod
    def create_connection():
        connection_id = str(uuid.uuid4())  # Unique ID
        return connection_id
