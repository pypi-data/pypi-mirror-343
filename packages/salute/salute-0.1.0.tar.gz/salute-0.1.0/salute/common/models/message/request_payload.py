from common.models.message.app_info import AppInfo
from common.models.message.payload import Payload
from common.models.message.text import Text


class RequestPayload(Payload):
    app_info: AppInfo
    message: Text
