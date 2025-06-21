from pydantic import Field

from ..enums import ChatType
from .base import BaleObject


class Chat(BaleObject):
    type: ChatType = Field(..., alias="1")
    id: int = Field(..., alias="2")
