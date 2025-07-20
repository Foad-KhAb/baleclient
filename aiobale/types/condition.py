from __future__ import annotations

from pydantic import Field
from typing import Optional

from .base import BaleObject
from .values import BoolValue


class Condition(BaleObject):
    excepted_permissions: Optional[BoolValue] = Field(None, alias="1")
    contacts: Optional[BoolValue] = Field(None, alias="2")
