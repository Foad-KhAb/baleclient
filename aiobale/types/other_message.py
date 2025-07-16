from pydantic import Field

from .base import BaleObject


class OtherMessage(BaleObject):
    date: int = Field(..., alias="1")
    message_id: int = Field(..., alias="2")
    seq: int = Field(0, alias="3")
