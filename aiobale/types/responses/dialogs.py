from __future__ import annotations

from pydantic import Field, model_validator
from typing import Any, Dict, List

from ..peer_data import PeerData
from ..base import BaleObject


class DialogResponse(BaleObject):
    dialogs: List[PeerData] = Field(default_factory=list, alias="3")
    
    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "3" not in data:
            return data
        
        if not isinstance(data["3"], list):
            data["3"] = [data["3"]]
        
        return data
