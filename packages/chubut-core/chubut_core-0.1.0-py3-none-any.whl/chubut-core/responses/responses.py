from http.client import HTTPResponse
import json
from http import HTTPStatus
from typing import Dict, Optional, Union
from fastapi import Response as FastApiResponse
from pydantic import BaseModel, ConfigDict, Field


def create_http_response(status_code: int, body: str) -> FastApiResponse:
    return FastApiResponse(
        status_code=status_code,
        content=body,
        media_type="application/json"
    )

class Response(BaseModel):
    def is_error(self):
        raise NotImplementedError

    def as_http_response(self) -> str:
        return self.as_json()

    def as_json(self):
        return self.model_dump()


class ErrorResponse(Response):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    errors: Optional[Union[str, Exception, Dict]] = Field(default=None)

    def __str__(self):
        return str(self.errors)

    def __repr__(self):
        return self.__str__()

    def is_error(self):
        return True

    def as_json(self):
        message = str(self.errors)
        if self.errors is None:
            message = "Internal Server Error"
        return json.dumps({"message": message})

    def as_http_response(self) -> HTTPResponse:
        return create_http_response(status_code=HTTPStatus.BAD_REQUEST, body=self.as_json())


class PartialResponse(Response):
    success: Optional[Union[str, Dict]] = Field(default=None)
    errors: Optional[Union[str, Dict]] = Field(default=None)
    
    def is_error(self):
        return False
    
    def as_json(self):
        return json.dumps({"success": self.success,
                           "errors": self.errors})
        
    def as_http_response(self) -> HTTPResponse:
        return create_http_response(status_code=HTTPStatus.PARTIAL_CONTENT, body=self.as_json())    


class SuccessResponse(Response):
    def is_error(self):
        return False