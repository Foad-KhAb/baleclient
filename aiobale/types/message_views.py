from __future__ import annotations

from pydantic import Field, model_validator
from typing import Any, Dict, List

from .base import BaleObject
from .other_message import OtherMessage


class MessageViews(BaleObject):
    message: OtherMessage = Field(..., alias="1")
    views: int = Field(..., alias="2")
    
    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["2"] = data["2"]["1"]
        return data
