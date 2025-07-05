from pydantic import Field
from typing import Optional, Any, List

from ..base import BaleObject
from ..user import UserAuth


class Value(BaleObject):
    value: str = Field(..., alias="1")


class ValidateCodeResponse(BaleObject):
    user: UserAuth = Field(..., alias="2")
    jwt: Value = Field(..., alias="4")
