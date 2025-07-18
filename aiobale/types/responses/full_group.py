from __future__ import annotations

from pydantic import Field

from ..base import BaleObject
from ..full_group import FullGroup


class FullGroupResponse(BaleObject):
    fullgroup: FullGroup = Field(None, alias="1")
