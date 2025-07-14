from pydantic import Field

from .base import BaleObject


class UserBlocked(BaleObject):
    user_id: int = Field(..., alias="1")
    
    
class UserUnblocked(BaleObject):
    user_id: int = Field(..., alias="1")
