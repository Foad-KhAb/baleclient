from __future__ import annotations

from pydantic import Field

from ..base import BaleObject


class InviteURLResponse(BaleObject):
    url: str = Field(..., alias="1")
