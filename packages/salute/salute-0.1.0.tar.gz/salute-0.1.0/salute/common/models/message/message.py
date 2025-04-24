from pydantic import BaseModel

from common.models.message.payload import Payload
from common.models.message.user import User
from common.models.message.name import Name


class Message(BaseModel):
    sessionId: str
    messageId: int
    messageName: Name
    payload: Payload
    uuid: User
