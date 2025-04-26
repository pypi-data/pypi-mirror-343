from enum import Enum


class EventCode(Enum):
    DO_SOMETHING = "DO_SOMETHING"
    DO_SOMETHING_RPC = "DO_SOMETHING_RPC"
    
class ExpectedServices(Enum):
    SERVICE_A = "SERVICE_A"
    SERVICE_B = "SERVICE_B"
    SERVICE_C = "SERVICE_C"
    
class ResponseStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"