from common.models.message.message import Message
from common.models.message.response_payload import ResponsePayload


class ResponseMessage(Message):
    payload: ResponsePayload
