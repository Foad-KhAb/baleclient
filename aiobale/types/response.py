from pydantic import Field
from typing import Any, Optional

from .base import BaleObject
from .update import UpdateBody


class BaleError(BaleObject):
    topic: int = Field(..., alias="1")
    message: str = Field(..., alias="2")


class ResponsetBody(BaleObject):
    error: Optional[BaleError] = Field(None, alias="1")
    result: Optional[Any] = Field(None, alias="2")
    number: int = Field(..., alias="3")
    

class UpdateField(BaleObject):
    body: UpdateBody = Field(..., alias="1")
    

class Response(BaleObject):
    response: Optional[ResponsetBody] = Field(None, alias="1")
    update: Optional[UpdateField] = Field(None, alias="2")
    auth: Optional[Any] = Field(None, alias="5")
