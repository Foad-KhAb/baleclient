from typing import Optional
from pydantic import Field

from .base import BaleObject


class Group(BaleObject):
    id: int = Field(..., alias="1")
    access_hash: Optional[int] = Field(None, alias="2")
