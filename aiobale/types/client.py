from pydantic import Field
from typing import List, Optional, Any

from .base import BaleObject


class ClientData(BaleObject):
    id: int = Field(..., alias="user_id")
    
    app_id: int
    auth_id: str
    auth_sid: int
    service: str
