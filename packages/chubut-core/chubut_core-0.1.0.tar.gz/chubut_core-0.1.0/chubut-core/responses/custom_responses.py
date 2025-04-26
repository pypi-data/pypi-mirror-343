from typing import Dict
from core.event_manager.enums import ResponseStatus
from .responses import SuccessResponse

class BeeneuResponse(SuccessResponse):
    status: ResponseStatus
    response: Dict

class SuccessPublish(SuccessResponse):
    message_id: str

class SuccessRpcCall(SuccessResponse):
    response: Dict
    errors: Dict | None = None