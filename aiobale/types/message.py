from __future__ import annotations

from pydantic import Field, model_validator
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from .chat import Chat
from .base import BaleObject
from ..enums import ChatType, ListLoadMode, ReportKind, TypingMode
from .quoted_message import QuotedMessage
from .message_content import MessageContent
from .other_message import OtherMessage
from .full_user import FullUser
from .user import User
from .message_reaction import MessageReactions
from .reaction_data import ReactionData

if TYPE_CHECKING:
    from .responses import DefaultResponse


class Message(BaleObject):
    chat: Chat = Field(..., alias="1")
    sender_id: int = Field(..., alias="2")
    date: int = Field(..., alias="3")
    message_id: int = Field(..., alias="4")
    content: MessageContent = Field(..., alias="5")
    quoted_replied_to: Optional[QuotedMessage] = Field(None, alias="7")
    previous_message: Optional[OtherMessage] = Field(None, alias="9")

    next_message: Optional[OtherMessage] = Field(None, exclude=True)
    replied_to: Optional[Message] = Field(None, exclude=True)

    if TYPE_CHECKING:

        def __init__(
            self,
            *,
            chat: Chat,
            sender_id: int,
            date: int,
            message_id: int,
            content: MessageContent,
            quoted_replied_to: Optional[QuotedMessage] = None,
            replied_to: Optional[Message] = None,
            previous_message: Optional[OtherMessage] = None,
            next_message: Optional[OtherMessage] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                chat=chat,
                sender_id=sender_id,
                date=date,
                message_id=message_id,
                content=content,
                replied_to=replied_to,
                quoted_replied_to=quoted_replied_to,
                previous_message=previous_message,
                next_message=next_message,
                **__pydantic_kwargs,
            )

    @model_validator(mode="after")
    def attach_chat_to_reply(self) -> Message:
        if self.quoted_replied_to and not self.quoted_replied_to.chat:
            self.quoted_replied_to.chat = self.chat

            if not self.replied_to:
                self.replied_to = self.quoted_replied_to.message

        return self

    @property
    def text(self) -> Optional[str]:
        text_content = self.content.text
        if text_content is None:
            return

        return text_content.value

    async def answer(self, text: str, message_id: Optional[int] = None) -> Message:

        return await self.client.send_message(
            text=text,
            chat_id=self.chat.id,
            chat_type=self.chat.type,
            message_id=message_id,
        )

    async def reply(self, text: str, message_id: Optional[int] = None) -> Message:

        return await self.client.send_message(
            text=text,
            chat_id=self.chat.id,
            chat_type=self.chat.type,
            reply_to=self,
            message_id=message_id,
        )

    async def edit_text(self, text: str) -> DefaultResponse:

        return await self.client.edit_message(
            text=text,
            message_id=self.message_id,
            chat_id=self.chat.id,
            chat_type=self.chat.type,
        )

    async def delete(self, just_me: Optional[bool] = False) -> DefaultResponse:

        return await self.client.delete_message(
            message_id=self.message_id,
            message_date=self.date,
            chat_id=self.chat.id,
            chat_type=self.chat.type,
            just_me=just_me,
        )

    async def forward_to(
        self, chat_id: int, chat_type: ChatType, new_id: Optional[int] = None
    ) -> DefaultResponse:

        return await self.client.forward_message(
            message=self, chat_id=chat_id, chat_type=chat_type, new_id=new_id
        )

    async def seen(self) -> DefaultResponse:
        return await self.client.seen_chat(
            chat_id=self.chat.id, chat_type=self.chat.type
        )

    async def clear_chat(self) -> DefaultResponse:
        return await self.client.clear_chat(
            chat_id=self.chat.id, chat_type=self.chat.type
        )

    async def delete_chat(self) -> DefaultResponse:
        return await self.client.delete_chat(
            chat_id=self.chat.id, chat_type=self.chat.type
        )

    async def load_history(
        self,
        limit: int = 20,
        offset_date: int = -1,
        load_mode: ListLoadMode = ListLoadMode.BACKWARD,
    ) -> List[Message]:

        return await self.client.load_history(
            chat_id=self.chat.id,
            chat_type=self.chat.type,
            limit=limit,
            offset_date=offset_date,
            load_mode=load_mode,
        )

    async def pin(self, just_me: bool = False) -> DefaultResponse:

        return await self.client.pin_message(
            message_id=self.message_id,
            message_date=self.date,
            chat_id=self.chat.id,
            chat_type=self.chat.type,
            just_me=just_me,
        )

    async def unpin(self) -> DefaultResponse:
        return await self.client.unpin_message(
            message_id=self.message_id,
            message_date=self.date,
            chat_id=self.chat.id,
            chat_type=self.chat.type,
        )

    async def unpin_all(self) -> DefaultResponse:
        return await self.client.unpin_all(
            one_message_date=self.date,
            one_message_id=self.message_id,
            chat_id=self.chat.id,
            chat_type=self.chat.type,
        )

    async def load_pinned_messages(self) -> List[Message]:
        return await self.client.load_pinned_messages(
            chat_id=self.chat.id, chat_type=self.chat.type
        )

    async def load_full_chat(self) -> FullUser:
        return await self.client.load_full_user(
            chat_id=self.chat.id, chat_type=self.chat.type
        )

    async def load_full_user(self) -> FullUser:
        return await self.client.load_full_user(
            chat_id=self.sender_id, chat_type=ChatType.PRIVATE
        )

    async def load_chat(self) -> User:
        return await self.client.load_user(
            chat_id=self.chat.id, chat_type=self.chat.type
        )

    async def load_user(self) -> User:
        return await self.client.load_user(
            chat_id=self.sender_id, chat_type=ChatType.PRIVATE
        )

    async def edit_local_name(self, name: str) -> DefaultResponse:
        return await self.client.edit_user_local_name(name=name, user_id=self.sender_id)

    async def block(self) -> DefaultResponse:
        return await self.client.block_user(user_id=self.sender_id)

    async def unblock(self) -> DefaultResponse:
        return await self.client.unblock_user(user_id=self.sender_id)

    async def add_as_contact(self) -> DefaultResponse:
        return await self.client.add_contact(user_id=self.sender_id)

    async def remove_contact(self) -> DefaultResponse:
        return await self.client.remove_contact(user_id=self.sender_id)

    async def report(
        self, kind: ReportKind = ReportKind.SPAM, reason: Optional[str] = None
    ) -> DefaultResponse:
        return await self.client.report_message(
            chat_id=self.chat.id,
            chat_type=self.chat.type,
            message=self,
            kind=kind,
            reason=reason,
        )

    async def report_chat(
        self, reason: Optional[str] = None, kind: ReportKind = ReportKind.SPAM
    ) -> DefaultResponse:
        return await self.client.report_chat(
            chat_id=self.chat.id, chat_type=self.chat.type, kind=kind, reason=reason
        )

    async def start_typing(
        self, typing_mode: TypingMode = TypingMode.TEXT
    ) -> DefaultResponse:
        return await self.client.start_typing(
            chat_id=self.chat.id, chat_type=self.chat.type, typing_mode=typing_mode
        )

    async def stop_typing(
        self, typing_mode: TypingMode = TypingMode.TEXT
    ) -> DefaultResponse:
        return await self.client.stop_typing(
            chat_id=self.chat.id, chat_type=self.chat.type, typing_mode=typing_mode
        )
        
    async def get_reactions(self) -> MessageReactions:
        return await self.client.get_message_reactions(
            message=self,
            chat_id=self.chat.id,
            chat_type=self.chat.type
        )
        
    async def get_reaction_list(
        self,
        emojy: str,
        page: int = 1,
        limit: int = 20
    ) -> List[ReactionData]:
        return await self.client.get_reaction_list(
            emojy=emojy,
            message=self,
            chat_id=self.chat.id,
            chat_type=self.chat.type,
            limit=limit,
            page=page
        )
