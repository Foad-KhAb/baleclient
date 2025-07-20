from pydantic import Field, model_validator
from typing import Dict, List, Optional, Any

from .base import BaleObject
from .int_bool import IntBool
from .permissions import Permissions
    

class Member(BaleObject):
    id: int = Field(..., alias="1")
    inviter_id: Optional[int] = Field(None, alias="2")
    date: Optional[int] = Field(None, alias="3")
    is_admin: IntBool = Field(False, alias="4")
    promoted_by: Optional[int] = Field(None, alias="5")
    promoted_at: Optional[int] = Field(None, alias="6")
    permissions: Optional[List[Permissions]] = Field(None, alias="7")
    
    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str , Any]:
        for key in list(data.keys()):
            value = data[key]
            
            if isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]

            elif not value:
                data.pop(key)
                
            elif "7" in data and not isinstance(data["7"], list):
                data["7"] = [data["7"]]
                
        return data
