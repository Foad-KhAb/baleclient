from typing import Any, Dict, List, Optional
from pydantic import Field, model_validator

from ..enums import GroupType, Restriction
from .base import BaleObject
from .int_bool import IntBool
from .permissions import Permissions


class Group(BaleObject):
    id: int = Field(..., alias="1")
    access_hash: Optional[int] = Field(None, alias="2")
    title: str = Field(..., alias="3")
    is_member: IntBool = Field(False, alias="5")
    is_hidden: IntBool = Field(False, alias="12")
    group_type: GroupType = Field(GroupType.GROUP, alias="15")
    can_send_message: IntBool = Field(False, alias="16")
    username: Optional[str] = Field(None, alias="17")
    is_orphaned: IntBool = Field(False, alias="18")
    members_count: int = Field(..., alias="20")
    permissions: Optional[Permissions] = Field(None, alias="30")
    default_permissions: Optional[Permissions] = Field(None, alias="31")
    owner_id: Optional[int] = Field(None, alias="32")
    available_reactions: List[str] = Field(default_factory=list, alias="33")
    is_suspend: IntBool = Field(False, alias="36")
    restriction: Restriction = Field(Restriction.PRIVATE, alias="40")
    
    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str , Any]:
        for key in list(data.keys()):
            value = data[key]
            
            if isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]

            elif not value:
                data.pop(key)

            elif key == "33" and not isinstance(data[key], list):
                data[key] = [data[key]]
                
        return data
