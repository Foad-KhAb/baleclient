from __future__ import annotations

from pydantic import Field, model_validator
from typing import List, Dict, Any

from ..base import BaleObject
from ..full_user import FullUser


class FullUsersResponse(BaleObject):
    data: List[FullUser] = Field(..., alias="1")
    
    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "1" not in data:
            return data
        
        if not isinstance(data["1"], list):
            data["1"] = [data["1"]]
        
        return data
    
    
class UsersResponse(BaleObject):
    data: List[FullUser] = Field(..., alias="1")
    
    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "1" not in data:
            return data
        
        if not isinstance(data["1"], list):
            data["1"] = [data["1"]]
        
        return data
