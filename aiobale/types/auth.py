from pydantic import Field
from typing import Optional

from .base import BaleObject


class AuthBody(BaleObject):
    authorized: int = Field(..., alias="1")
    ready: int = Field(..., alias="2")
    

class Auth(BaleObject):
    client: Optional[AuthBody] = Field(None, alias="3")
    server: Optional[AuthBody] = Field(None, alias="5")
