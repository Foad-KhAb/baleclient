from __future__ import annotations

from pydantic import Field, field_serializer
from typing import TYPE_CHECKING, Optional

from .base import BaleObject
from .message_content import MessageContent
from .peer import Peer
from .chat import Chat
from .values import IntValue

if TYPE_CHECKING:
    from .message import Message


class UpdatedMessage(BaleObject):
    peer: Peer = Field(..., alias="1")
    message_id: int = Field(..., alias="2")
    content: MessageContent = Field(..., alias="3")
    date: IntValue = Field(..., alias="4")
    sender_id: IntValue = Field(..., alias="5")
    
    @property
    def message(self) -> Message:
        from .message import Message
        
        chat = Chat(id=self.peer.id, type=self.peer.type)
        
        return Message(
            message_id=self.message_id,
            chat=chat,
            sender_id=self.sender_id.value,
            date=self.date.value,
            content=self.content,
                 
        ).as_(self.client)
        
    @field_serializer
    def return_message(self) -> Message:
        return self.message
