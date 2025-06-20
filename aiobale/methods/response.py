from pydantic import Field
from typing import Any, Optional

from .base import BaleMethod


class BaleError(BaleMethod):
    topic: int
    message: str


class ResponsetBody(BaleMethod):
    error: Optional[BaleError] = Field(..., alias="1")
    result: Optional[Any] = Field(..., alias="2")
    number: int = Field(..., alias="3")
    

class Response(BaleMethod):
    body: ResponsetBody = Field(..., alias="1")
