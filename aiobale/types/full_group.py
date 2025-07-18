from typing import Any, Dict, List, Optional
from pydantic import Field, model_validator

from ..enums import GroupType, PrivacyMode
from .base import BaleObject
from .int_bool import IntBool
from .full_user import ExInfo
from .member import Member
from .permissions import Permissions


class FullGroup(BaleObject):
    id: int = Field(..., alias="1")
    access_hash: Optional[int] = Field(None, alias="2")
    title: str = Field(..., alias="3")
    owner_id: int = Field(..., alias="5")
    created_at: int = Field(..., alias="6")
    group_type: GroupType = Field(GroupType.GROUP, alias="7")
    is_joined: IntBool = Field(False, alias="7")
    member_count: int = Field(..., alias="10")
    username: Optional[str] = Field(None, alias="11")
    is_orphaned: IntBool = Field(False, alias="12")
    permissions: Permissions = Field(..., alias="13")
    default_permissions: Permissions = Field(..., alias="14")
    
    about: Optional[str] = Field(None, alias="16")
    members: Optional[List[Member]] = Field(None, alias="17")
    ex_info: ExInfo = Field(..., alias="18")
    available_reactions: List[str] = Field([], alias="24")
    is_suspend: IntBool = Field(False, alias="25")
    privacy_mode: PrivacyMode = Field(..., alias="28")
    
    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str , Any]:
        for key in list(data.keys()):
            value = data[key]
            
            if key in ["18", "13", "14"]:
                continue

            elif isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]

            elif not value:
                data.pop(key)

            elif key == "4" and not isinstance(data[key], list):
                data[key] = [data[key]]
                
        return data
