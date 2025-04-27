from h_message_bus import NatsPublisherAdapter

class HaiService:
    def __init__(self, nats_publisher_adapter: NatsPublisherAdapter):
        self.nats_publisher_adapter = nats_publisher_adapter


