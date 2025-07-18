from __future__ import annotations

from pydantic import Field

from .base import BaleObject


class ReactionData(BaleObject):
    user_id: int = Field(..., alias="1")
    emojy: str = Field(..., alias="2")
    data: int = Field(..., alias="3")
