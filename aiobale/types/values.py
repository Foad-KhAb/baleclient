from pydantic import Field
from typing import Optional

from .base import BaleObject
from .int_bool import IntBool


class StringValue(BaleObject):
    value: str = Field(..., alias="1")


class IntValue(BaleObject):
    value: int = Field(..., alias="1")


class BoolValue(BaleObject):
    value: IntBool = Field(..., alias="1")


class BytesValue(BaleObject):
    value: bytes = Field(..., alias="1")
