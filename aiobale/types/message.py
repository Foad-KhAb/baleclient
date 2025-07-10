from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING, Optional

from .chat import Chat
from .base import BaleObject
from ..enums import ChatType
from .quoted_message import QuotedMessage
from .message_content import MessageContent

if TYPE_CHECKING:
    from .responses import DefaultResponse, MessageResponse


class PrevMessage(BaleObject):
    date: int = Field(..., alias="1")
    message_id: int = Field(..., alias="2")


class Message(BaleObject):
    chat: Chat = Field(..., alias="1")
    sender_id: int = Field(..., alias="2")
    date: int = Field(..., alias="3")
    message_id: int = Field(..., alias="4")
    content: MessageContent = Field(..., alias="5")
    replied_to: Optional[QuotedMessage] = Field(None, alias="7")
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
            
    @property
    def text(self) -> Optional[str]:
        text_content = self.content.text
        if text_content is None:
            return
        
        return text_content.value
    
    async def answer(
        self,
        text: str,
        message_id: Optional[int] = None
    ) -> MessageResponse:
        
        return await self.client.send_message(
            text=text,
            chat_id=self.chat.id,
            chat_type=self.chat.type,
            message_id=message_id
        )
        
    async def reply(
        self,
        text: str,
        message_id: Optional[int] = None
    ) -> MessageResponse:
        
        return await self.client.send_message(
            text=text,
            chat_id=self.chat.id,
            chat_type=self.chat.type,
            reply_to=self,
            message_id=message_id
        )

    async def delete(
        self, 
        just_me: Optional[bool] = False
    ) -> DefaultResponse:

        return await self.client.delete_message(
            message_id=self.message_id,
            message_date=self.date,
            chat_id=self.chat.id,
            chat_type=self.chat.type,
            just_me=just_me
        )
        
    async def forward_to(
        self,
        chat_id: int,
        chat_type: ChatType,
        new_id: Optional[int] = None
    ) -> DefaultResponse:
        
        return await self.client.forward_message(
            message=self,
            chat_id=chat_id,
            chat_type=chat_type,
            new_id=new_id
        )
        
    async def seen(self) -> DefaultResponse:

        return await self.client.seen_chat(
            chat_id=self.chat.id,
            chat_type=self.chat.type
        )
