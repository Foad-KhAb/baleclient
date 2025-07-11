from pydantic import Field
from typing import TYPE_CHECKING, Any, Optional

from ..types import Peer, MessageContent
from ..types.responses import DefaultResponse
from ..enums import Services
from .base import BaleMethod


class UpdateMessage(BaleMethod):
    __service__ = Services.MESSAGING.value
    __method__ = "UpdateMessage"
    
    __returning__ = DefaultResponse
    
    peer: Peer = Field(..., alias="1")
    message_id: int = Field(..., alias="2")
    updated_message: MessageContent = Field(..., alias="3")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message_id: int,
            updated_message: MessageContent,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                peer=peer,
                message_id=message_id,
                updated_message=updated_message
                **__pydantic_kwargs
            )
