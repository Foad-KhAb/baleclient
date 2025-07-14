from pydantic import Field, model_validator
from typing import Dict, List, Optional, Any

from .base import BaleObject
from .int_bool import IntBool
from .full_user import ExInfo
    

class Value(BaleObject):
    value: str = Field(..., alias="1")


class UserAuth(BaleObject):
    id: int = Field(..., alias="1")
    access_hash: int = Field(..., alias="2")
    name: str = Field(..., alias="3")
    username: Optional[Value] = Field(None, alias="9")
    

class User(BaleObject):
    id: int = Field(..., alias="1")
    access_hash: int = Field(..., alias="2")
    name: str = Field(..., alias="3")
    local_name: Optional[str] = Field(None, alias="4")
    sex: Optional[int] = Field(None, alias="5")
    is_bot: IntBool = Field(False, alias="7")
    username: Optional[str] = Field(None, alias="9")
    is_deleted: IntBool = Field(False, alias="16")
    created_at: int = Field(..., alias="19")
    ex_info: ExInfo = Field(..., alias="20")
    
    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str , Any]:
        for key in list(data.keys()):
            value = data[key]
            
            if key == "20":
                continue

            elif isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]

            elif not value:
                data.pop(key)
                
        return data
