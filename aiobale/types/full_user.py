from typing import List, Optional
from pydantic import Field

from ..enums import ChatType
from .int_bool import IntBool
from .base import BaleObject


class ExInfo(BaleObject):
    expeer_type: ChatType = Field(..., alias="1")
    identified: IntBool = Field(False, alias="2")


class FullUser(BaleObject):
    id: int = Field(..., alias="1")
    about: Optional[str] = Field(None, alias="3")
    languages: Optional[List[str]] = Field(None, alias="4")
    ex_info: ExInfo = Field(..., alias="9")
    created_at: int = Field(..., alias="15")
    privacy_mode: int = Field(..., alias="16")
