from __future__ import annotations

from pydantic import Field

from ..base import BaleObject
from ..group import Group


class GroupResponse(BaleObject):
    group: Group = Field(None, alias="1")
