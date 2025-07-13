from typing import Any, Dict, Optional
from pydantic import Field, model_validator

from .base import BaleObject
from .peer import Peer
from .message_content import MessageContent
from .message import Message
from .chat import Chat


class PeerData(BaleObject):
    peer: Peer = Field(..., alias="1")
    unread_count: int = Field(2, alias="2")
    sort_date: int = Field(..., alias="3")
    sender_id: int = Field(..., alias="4")
    message_id: int = Field(..., alias="5")
    date: int = Field(..., alias="6")
    content: MessageContent = Field(..., alias="7")
    first_unread_message: int = Field(..., alias="9")
    unread_mentions: int = Field(..., alias="13")
    
    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["9"] = data["9"]["1"]
        data["13"] = data["13"]["1"]
        
        return data
    
    @property
    def message(self) -> Message:
        chat = Chat(id=self.peer.id, type=self.peer.type)
        
        return Message(
            chat=chat,
            sender_id=self.sender_id,
            date=self.date,
            message_id=self.message_id,
            content=self.content
            
        ).as_(self.client)
