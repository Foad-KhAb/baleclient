from pydantic import Field
from typing import Optional, Any

from .base import BaleObject
from ..enums import SendCodeType


class AuthBody(BaleObject):
    authorized: int = Field(..., alias="1")
    ready: int = Field(..., alias="2")
