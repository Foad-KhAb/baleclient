from pydantic import Field
from typing import List, Optional, Any

from .base import BaleObject
from .user import UserAuth


class ClientData(BaleObject):
    id: int = Field(..., alias="user_id")
    user: UserAuth
    
    app_id: int
    auth_id: str
    auth_sid: int
    service: str
