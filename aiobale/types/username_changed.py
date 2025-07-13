from pydantic import Field, model_validator
from typing import Any, Dict

from .base import BaleObject


class UsernameChanged(BaleObject):
    user_id: int = Field(..., alias="1")
    username: str = Field(..., alias="2")
    
    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["2"] = data["2"]["1"]
        
        return data
