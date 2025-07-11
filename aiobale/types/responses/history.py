from __future__ import annotations

from pydantic import Field
from typing import List

from ..message_data import MessageData
from ..base import BaleObject
from ..chat import Chat


class HistoryResponse(BaleObject):
    result: List[MessageData] = Field(..., alias="1")
    
    def _add_chat_to_message(self, message: MessageData, chat: Chat):
        message.chat = chat
        if message.replied_to is not None:
            self._add_chat_to_message(message.replied_to, chat)

    def add_chat(self, chat: Chat) -> None:
        for message in self.result:
            self._add_chat_to_message(message, chat)
