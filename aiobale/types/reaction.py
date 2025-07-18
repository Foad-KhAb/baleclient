from __future__ import annotations

from pydantic import Field, model_validator
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..utils import Int64VarintCodec
from .base import BaleObject


class Reaction(BaleObject):
    users: List[int] = Field([], alias="1")
    emojy: str = Field(..., alias="2")
    count: int = Field(..., alias="3")
    
    @model_validator(mode="before")
    @classmethod
    def validate_input(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "1" in data:
            data["1"] = Int64VarintCodec.decode_list(data["1"])
            
        data["3"] = data["3"]["1"]
        
        return data
