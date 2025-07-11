from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING, Optional

from ..exceptions import AiobaleError
from .other_message import OtherMessage
from .base import BaleObject
from .message_content import MessageContent
from .quoted_message import QuotedMessage
from .chat import Chat

if TYPE_CHECKING:
    from .message import Message


class MessageData(BaleObject):
    sender_id: int = Field(..., alias="1")
    message_id: int = Field(..., alias="2")
    date: int = Field(..., alias="3")
    content: MessageContent = Field(..., alias="4")
    replied_to: Optional[QuotedMessage] = Field(None, alias="8")
    previous_message: Optional[OtherMessage] = Field(None, alias="10")
    next_message: Optional[OtherMessage] = Field(None, alias="11")
    
    chat: Optional[Chat] = Field(None, exclude=True)
    
    @property
    def message(self) -> Message:
        from .message import Message
        
        if self.chat is None:
            raise AiobaleError("Need the current chat to process")
        
        return Message(
            message_id=self.message_id,
            chat=self.chat,
            sender_id=self.sender_id,
            date=self.date,
            content=self.content,
            
            
        ).as_(self.client)
