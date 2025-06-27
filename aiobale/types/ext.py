from pydantic import Field
from typing import List, Optional, Any

from .base import BaleObject


class ExtValue(BaleObject):
    string: Optional[str] = Field(None, alias="1")
    number: Optional[int] = Field(None, alias="4")


class ExtData(BaleObject):
    name: str = Field(..., alias="1")
    value: ExtValue = Field(..., alias="2")
