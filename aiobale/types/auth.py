from pydantic import Field
from typing import Optional

from .base import BaleObject


class AuthBody(BaleObject):
    authorized: int = Field(..., alias="1")
    ready: int = Field(..., alias="2")
