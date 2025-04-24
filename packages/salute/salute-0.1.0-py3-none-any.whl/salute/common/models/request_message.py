from common.models.message.message import Message
from common.models.message.request_payload import RequestPayload


class RequestMessage(Message):
    payload: RequestPayload

    def get_intent(self) -> str:
        if not self.payload.intent:
            return ""
        return self.payload.intent.lower()

    def get_user_id(self) -> str:
        return self.uuid.userId
