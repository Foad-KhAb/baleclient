from pydantic import Field
from typing import Any, Optional

from .base import BaleObject
from .message import Message


class Update(BaleObject):
    message: Optional[Message] = Field(None, alias="55")


class UpdateBody(BaleObject):
    body: Any = Field(..., alias="1")
    update_id: int = Field(..., alias="2")
    date: int = Field(..., alias="3")
