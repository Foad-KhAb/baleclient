from __future__ import annotations

from pydantic import Field, model_validator
from typing import Dict, Any, Optional

from ..base import BaleObject
from ..full_group import FullGroup


class FullGroupResponse(BaleObject):
    fullgroup: Optional[FullGroup] = Field(None, alias="1")
    
    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "1" not in data:
            return data
        
        elif not data["1"]:
            data.pop("1")
            
        return data
