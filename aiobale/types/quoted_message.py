from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING, Optional

from .peer import Peer
from .values import IntValue
from .base import BaleObject
from .message_content import MessageContent
from .chat import Chat

if TYPE_CHECKING:
    from .message import Message


class QuotedMessage(BaleObject):
    message_id: IntValue = Field(..., alias="1")
    sender_id: int = Field(..., alias="3")
    date: int = Field(..., alias="4")
    content: MessageContent = Field(..., alias="5")
    peer: Peer = Field(..., alias="6")
    
    @property
    def message(self) -> Message:
        from .message import Message
        
        chat = Chat(id=self.peer.id, type=self.peer.type)
        return Message(
            message_id=self.message_id.value,
            chat=chat,
            sender_id=self.sender_id,
            date=self.date,
            content=self.content
        ).as_(self.client)
