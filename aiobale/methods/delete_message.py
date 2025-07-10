from pydantic import Field
from typing import TYPE_CHECKING, Any, List

from ..types import Chat, Peer, MessageContent, IntValue
from ..types.responses import MessageResponse
from ..enums import Services
from .base import BaleMethod


class DeleteMessage(BaleMethod):
    __service__ = Services.MESSAGING.value
    __method__ = "DeleteMessage"
    
    __returning__ = MessageResponse
    
    peer: Peer = Field(..., alias="1")
    message_ids: List[int] = Field(..., alias="2")
    dates: List[int] = Field(..., alias="3")
    just_me: IntValue = Field(..., alias="4")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message_ids: List[int],
            dates: List[int],
            just_me: IntValue,
            **__pydantic_kwargs: Any
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                peer=peer,
                message_ids=message_ids,
                dates=dates,
                just_me=just_me,
                **__pydantic_kwargs
            )
