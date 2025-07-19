from pydantic import Field, model_validator
from typing import Any, Dict, Optional

from .base import BaleObject


class UsernameChanged(BaleObject):
    user_id: int = Field(..., alias="1")
    username: Optional[str] = Field(None, alias="2")
    
    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "2" not in data:
            return data
        
        data["2"] = data["2"]["1"]
        
        return data


class AboutChanged(BaleObject):
    user_id: int = Field(..., alias="1")
    about: str = Field(..., alias="2")
    
    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["2"] = data["2"]["1"]
        
        return data
