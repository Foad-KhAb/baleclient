from __future__ import annotations

from pydantic import Field, field_serializer, model_validator
from typing import List, Any, Dict

from .default import DefaultResponse
from ...types import InfoPeer


class ContactsResponse(DefaultResponse):
    peers: List[InfoPeer] = Field(..., alias="4")

    @model_validator(mode="before")
    @classmethod
    def add_message(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "4" not in data:
            return data

        if not isinstance(data["4"], list):
            data["4"] = [data["4"]]
            
        return data
    
    @field_serializer(mode="plain")
    def serializer(self):
        return self.peers
