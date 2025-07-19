from typing import Optional
from pydantic import Field

from .base import BaleObject


class ShortPeer(BaleObject):
    id: int = Field(..., alias="1")
    access_hash: int = Field(1, alias="2")
