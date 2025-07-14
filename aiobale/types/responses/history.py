from __future__ import annotations

from pydantic import Field, model_validator
from typing import List, Dict, Any

from ..message_data import MessageData
from ..base import BaleObject
from ..chat import Chat


class HistoryResponse(BaleObject):
    data: List[MessageData] = Field(..., alias="1")
    
    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "1" not in data:
            return data
            
        if not isinstance(data["1"], list):
            data["1"] = [data["1"]]
        
        return data
    
    def add_chat(self, chat: Chat) -> None:
        for message in self.data:
            message.chat = chat
            if message.replied_to is not None:
                message.replied_to.chat = chat
