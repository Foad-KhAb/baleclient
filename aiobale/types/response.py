from pydantic import Field
from typing import Any, Optional

from .base import BaleObject


class BaleError(BaleObject):
    code: int
    message: str


class ResponsetBody(BaleObject):
    error: Optional[BaleError] = Field(..., alias="1")
    result: Optional[Any] = Field(..., alias="2")
    number: int = Field(..., alias="3")
    

class Response(BaleObject):
    body: ResponsetBody = Field(..., alias="1")
