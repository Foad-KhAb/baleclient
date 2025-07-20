from __future__ import annotations

from typing import Any, Dict, List
from pydantic import Field, model_validator

from ...enums import ChatType
from ..message_data import MessageData
from ..message import Message
from ..short_peer import ShortPeer
from ..chat import Chat
from ..base import BaleObject


class GetPinsResponse(BaleObject):
    pins_data: List[MessageData] = Field(default_factory=list, alias="1")
    count: int = Field(0, alias="2")
    
    method_data: Any
    pins: List[Message] = []

    @model_validator(mode="before")
    @classmethod
    def normalize_lists(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        value = data.get("1")
        if value is not None and not isinstance(value, list):
            data["1"] = [value]
        return data
    
    @model_validator(mode="after")
    def add_message(self):
        group = getattr(self.method_data, "group")
        if not group or not isinstance(group, ShortPeer):
            return self
        
        for pinned in self.pins_data:
            pinned.chat = Chat(id=group.id, type=ChatType.GROUP)
            
        # Prevent infinite loop: bypass Pydantic
        object.__setattr__(self, "pins", [pin.message for pin in self.pins_data])
        return self
