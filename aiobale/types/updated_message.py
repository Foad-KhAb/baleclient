from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING, Optional

from ..exceptions import AiobaleError
from .other_message import OtherMessage
from .base import BaleObject
from .message_content import MessageContent
from .quoted_message import QuotedMessage
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
            sender_id=self.sender_id,
            date=self.date,
            content=self.content,
                 
        ).as_(self.client)
