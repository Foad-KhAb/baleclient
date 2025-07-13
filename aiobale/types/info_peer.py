from typing import Optional
from pydantic import Field

from ..enums import ChatType
from .base import BaleObject


class InfoPeer(BaleObject):
    id: int = Field(..., alias="1")
    type: ChatType = Field(..., alias="2")
