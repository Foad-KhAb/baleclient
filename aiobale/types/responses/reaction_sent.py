from __future__ import annotations

from pydantic import Field, model_validator
from typing import List, Any, Dict

from ..base import BaleObject
from ..reaction import Reaction


class ReactionSentResponse(BaleObject):
    reactions: List[Reaction] = Field(default_factory=list, alias="2")
    
    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "2" not in data:
            return data
        
        if not isinstance(data["2"], list):
            data["2"] = [data["2"]]
        
        return data
