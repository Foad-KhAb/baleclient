from typing import Optional
from pydantic import Field

from .base import BaleObject


class OtherMessage(BaleObject):
    date: int = Field(..., alias="1")
    message_id: int = Field(..., alias="2")
    seq: Optional[int] = Field(None, alias="3")
