from core.event_manager.enums import EventCode, ExpectedServices
from core.models import UUIDModel
from typing import Dict, List, Any
from uuid import uuid4
from pydantic import BaseModel

class GeneratedEvent(UUIDModel):
    expected_services: List[ExpectedServices] | None = None
    response_service: ExpectedServices | None = None
    correlation_uuid: str = str(uuid4())
    event_code: EventCode
    message: str
    user: str
    
class EventDispatcher(BaseModel):
    events: Dict[EventCode, Any]