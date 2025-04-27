from h_message_bus import NatsPublisherAdapter
from h_message_bus.domain.request_messages.vector_read_metadata_request_message import VectorReadMetaDataRequestMessage
from h_message_bus.domain.request_messages.vector_read_metadata_response_message import VectorReadMetaDataResponseMessage

class HaiService:
    def __init__(self, nats_publisher_adapter: NatsPublisherAdapter):
        self.nats_publisher_adapter = nats_publisher_adapter

    async def get_knowledgebase_metadata(self) -> VectorReadMetaDataResponseMessage:
        message = VectorReadMetaDataRequestMessage.create_message()
        response = await self.nats_publisher_adapter.request(message)
        metadata_result = VectorReadMetaDataResponseMessage.from_hai_message(response)
        return metadata_result
