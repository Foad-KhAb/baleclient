from pydantic import Field
from typing import TYPE_CHECKING, List

from ...types import Peer
from ...types.responses import ReactionSentResponse
from ...enums import Services
from ..base import BaleMethod


class MessageRemoveReaction(BaleMethod):
    __service__ = Services.ABACUS.value
    __method__ = "MessageRemoveReaction"
    
    __returning__ = ReactionSentResponse
    
    peer: Peer = Field(..., alias="1")
    message_id: int = Field(..., alias="2")
    emojy: str = Field(..., alias="3")
    date: int = Field(..., alias="4")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message_id: int,
            date: int,
            emojy: str,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                peer=peer,
                message_id=message_id,
                date=date,
                emojy=emojy,
                **__pydantic_kwargs
            )
