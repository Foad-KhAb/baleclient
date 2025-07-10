from pydantic import Field
from typing import TYPE_CHECKING, Any, Optional

from ..types import Chat, Peer, MessageContent, InfoMessage
from ..types.responses import MessageResponse
from ..enums import Services
from .base import BaleMethod


class SendMessage(BaleMethod):
    __service__ = Services.MESSAGING.value
    __method__ = "SendMessage"
    
    __returning__ = MessageResponse
    
    peer: Peer = Field(..., alias="1")
    message_id: int = Field(..., alias="2")
    content: MessageContent = Field(..., alias="3")
    reply_to: Optional[InfoMessage] = Field(None, alias="5")
    chat: Chat = Field(..., alias="6")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message_id: int,
            content: MessageContent,
            reply_to: InfoMessage,
            chat: Chat,
            **__pydantic_kwargs: Any
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                peer=peer,
                message_id=message_id,
                content=content,
                reply_to=reply_to,
                chat=chat,
                **__pydantic_kwargs
            )
