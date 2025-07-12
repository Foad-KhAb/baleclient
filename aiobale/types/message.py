from __future__ import annotations

from pydantic import Field, model_validator
from typing import TYPE_CHECKING, Optional

from .chat import Chat
from .base import BaleObject
from ..enums import ChatType, ListLoadMode
from .quoted_message import QuotedMessage
from .message_content import MessageContent
from .other_message import OtherMessage

if TYPE_CHECKING:
    from .responses import DefaultResponse, MessageResponse, HistoryResponse


class Message(BaleObject):
    chat: Chat = Field(..., alias="1")
    sender_id: int = Field(..., alias="2")
    date: int = Field(..., alias="3")
    message_id: int = Field(..., alias="4")
    content: MessageContent = Field(..., alias="5")
    replied_to: Optional[QuotedMessage] = Field(None, alias="7")
    previous_message: Optional[OtherMessage] = Field(None, alias="9")
    
    if TYPE_CHECKING:
        def __init__(
            self,
            *,
            chat: Chat,
            sender_id: int,
            date: int,
            message_id: int,
            content: MessageContent,
            replied_to: Optional[QuotedMessage] = None,
            previous_message: Optional[OtherMessage] = None
        ) -> None:
            super().__init__(
                chat=chat,
                sender_id=sender_id,
                date=date,
                message_id=message_id,
                content=content,
                replied_to=replied_to,
                previous_message=previous_message
            )
            
    @model_validator(mode="after")
    def attach_chat_to_reply(self) -> Message:
        if self.replied_to and not self.replied_to.chat:
            self.replied_to.chat = self.chat
        return self
            
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
        
    async def edit_text(self, text: str) -> DefaultResponse:
        
        return await self.client.edit_message(
            text=text,
            message_id=self.message_id,
            chat_id=self.chat.id,
            chat_type=self.chat.type
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
        
    async def clear_chat(self) -> DefaultResponse:
        return await self.client.clear_chat(
            chat_id=self.chat.id,
            chat_type=self.chat.type
        )
        
    async def delete_chat(self) -> DefaultResponse:
        return await self.client.delete_chat(
            chat_id=self.chat.id,
            chat_type=self.chat.type
        )
        
    async def load_history(
        self,
        limit: int = 20,
        offset_date: int = -1,
        load_mode: ListLoadMode = ListLoadMode.BACKWARD
    ) -> HistoryResponse:
        
        return await self.client.load_history(
            chat_id=self.chat.id,
            chat_type=self.chat.type,
            limit=limit,
            offset_date=offset_date,
            load_mode=load_mode
        )
        
    async def pin(
        self,
        just_me: bool = False
    ) -> DefaultResponse:
        
        return await self.client.pin_message(
            message_id=self.message_id,
            message_date=self.date,
            chat_id=self.chat.id,
            chat_type=self.chat.type,
            just_me=just_me
        )
