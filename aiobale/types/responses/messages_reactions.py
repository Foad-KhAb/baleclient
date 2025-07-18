from __future__ import annotations

from pydantic import Field, model_validator
from typing import List, Any, Dict

from ..base import BaleObject
from ..message_reaction import MessageReactions


class ReactionsResponse(BaleObject):
    messages: List[MessageReactions] = Field(default_factory=list, alias="1")
    
    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "1" not in data:
            return data
        
        if not isinstance(data["1"], list):
            data["1"] = [data["1"]]
        
        return data
