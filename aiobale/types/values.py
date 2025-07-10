from pydantic import Field
from typing import Optional

from .base import BaleObject


class StringValue(BaleObject):
    value: str = Field(None, alias="1")


class IntValue(BaleObject):
    value: int = Field(None, alias="1")
