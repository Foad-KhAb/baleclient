from pydantic import Field
from typing import Optional, Any

from .chat import Chat
from .base import BaleObject


class MessageContent(BaleObject):
    document = Field(..., alias="4")
    text = Field(..., alias="15")
    
    
class PrevMessage(BaleObject):
    unix_time: int = Field(..., alias="1")
    message_id: int = Field(..., alias="2")


class Message(BaleObject):
    chat: Chat = Field(..., alias="1")
    sender_id: int = Field(..., alias="2")
    unix_time: int = Field(..., alias="3")
    message_id: int = Field(..., alias="4")
    content: MessageContent = Field(..., alias="5")
    previous_message: PrevMessage = Field(..., alias="9")
