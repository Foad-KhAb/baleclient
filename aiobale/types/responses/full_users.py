from __future__ import annotations

from pydantic import Field, model_validator
from typing import List, Dict, Any

from ..message_data import MessageData
from ..base import BaleObject
from ..chat import Chat


class FullUsersResponse(BaleObject):
    data: List[MessageData] = Field(..., alias="1")
    
    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "1" in data:
            return data
        
        if not isinstance(data["1"], list):
            data["1"] = [data["1"]]
        
        return data
