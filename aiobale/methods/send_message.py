from pydantic import Field
from typing import TYPE_CHECKING, Any

from ..types import Chat, Peer, MessageContent
from ..types.responses import MessagetResponse
from ..enums import Services
from .base import BaleMethod


class SendMessage(BaleMethod):
    __service__ = Services.MESSAGING
    __method__ = "SendMessage"
    
    __returning__ = MessagetResponse
    
    peer: Peer = Field(..., alias="1")
    message_id: int = Field(..., alias="2")
    content: MessageContent = Field(..., alias="3")
    chat: Chat = Field(..., alias="6")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message_id: int,
            content: MessageContent,
            chat: Chat,
            **__pydantic_kwargs: Any
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                peer=peer,
                message_id=message_id,
                content=content,
                chat=chat,
                **__pydantic_kwargs
            )
