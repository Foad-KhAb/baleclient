from pydantic import Field
from typing import Any, Optional

from .base import BaleObject


class BaleError(BaleObject):
    topic: int
    message: str


class ResponsetBody(BaleObject):
    error: Optional[BaleError] = Field(None, alias="1")
    result: Optional[Any] = Field(None, alias="2")
    number: int = Field(..., alias="3")
    

class Response(BaleObject):
    response: ResponsetBody = Field(..., alias="1")
    update: Any = Field(..., alias="2")
