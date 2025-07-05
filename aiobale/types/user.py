from pydantic import Field
from typing import List, Optional, Any

from .ext import ExtData
from .base import BaleObject
from .auth import AuthBody
    

class Value(BaleObject):
    value: str = Field(..., alias="1")

class UserAuth(BaleObject):
    id: int = Field(..., alias="1")
    access_hash: int = Field(..., alias="2")
    name: str = Field(..., alias="3")
    username: Optional[Value] = Field(None, alias="9")
