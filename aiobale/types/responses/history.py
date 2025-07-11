from __future__ import annotations

from pydantic import Field, model_validator
from typing import List, Dict, Any

from ..message_data import MessageData
from ..base import BaleObject
from ..chat import Chat


class HistoryResponse(BaleObject):
    result: List[MessageData] = Field(..., alias="1")
    
    @model_validator(mode="before")
    def validate_list(cls, data: Dict[str, Any]):
        if not isinstance(data["1"], dict):
            data["1"] = list(data["1"])
        
        return data
    
    def _add_chat_to_message(self, message: MessageData, chat: Chat):
        message.chat = chat
        if message.replied_to is not None:
            self._add_chat_to_message(message.replied_to, chat)

    def add_chat(self, chat: Chat) -> None:
        for message in self.result:
            self._add_chat_to_message(message, chat)
