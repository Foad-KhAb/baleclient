from pydantic import Field
from typing import TYPE_CHECKING, Optional, Any

from .chat import Chat
from .base import BaleObject


class TextMessage(BaleObject):
    content: str = Field(..., alias="1")
    

class MessageCaption(BaleObject):
    content: Optional[str] = Field(None, alias="1")
    mentions: Optional[list | dict] = Field({}, alias="2")
    ext: Optional[dict] = Field({}, alias="3")
    

class DocumentMessage(BaleObject):
    file_id: int = Field(..., alias="1")
    access_hash: int = Field(..., alias="2")
    file_size: int = Field(..., alias="3")
    name: str = Field(..., alias="4")
    mime_type: str = Field(..., alias="5")
    ext: str = Field(..., alias="7")
    caption: MessageCaption = Field(..., alias="8")


class MessageContent(BaleObject):
    document: Optional[DocumentMessage] = Field(None, alias="4")
    text: Optional[TextMessage] = Field(None, alias="15")


class PrevMessage(BaleObject):
    date: int = Field(..., alias="1")
    message_id: int = Field(..., alias="2")


class Message(BaleObject):
    chat: Chat = Field(..., alias="1")
    sender_id: int = Field(..., alias="2")
    date: int = Field(..., alias="3")
    message_id: int = Field(..., alias="4")
    content: MessageContent = Field(..., alias="5")
    previous_message: Optional[PrevMessage] = Field(None, alias="9")
    
    if TYPE_CHECKING:
        def __init__(
            self,
            *,
            chat: Chat,
            sender_id: int,
            date: int,
            message_id: int,
            content: MessageContent,
            previous_message: Optional[PrevMessage]
        ) -> None:
            super().__init__(
                chat=chat,
                sender_id=sender_id,
                date=date,
                message_id=message_id,
                content=content,
                previous_message=previous_message
            )
