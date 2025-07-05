from pydantic import Field
from typing import Optional, Any, List

from ..int_bool import IntBool
from ..base import BaleObject
from ...enums import SendCodeType


class Value(BaleObject):
    value: str = Field(..., alias="1")


class ValidateCodeResponse(BaleObject):
    user: dict = Field(..., alias="2")
    jwt: Value = Field(..., alias="4")
