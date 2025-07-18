from __future__ import annotations

from pydantic import Field
from typing import List

from .base import BaleObject
from .reaction import Reaction


class MessageReactions(BaleObject):
    id: int = Field(..., alias="1")
    date: int = Field(..., alias="2")
    reactions: List[Reaction] = Field([], alias="3")
