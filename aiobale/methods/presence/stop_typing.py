from pydantic import Field
from typing import TYPE_CHECKING

from ...types import Peer
from ...types.responses import DefaultResponse
from ...enums import Services, TypingMode
from ..base import BaleMethod


class StopTyping(BaleMethod):
    __service__ = Services.PRESENCE.value
    __method__ = "StopTyping"
    
    __returning__ = DefaultResponse
    
    peer: Peer = Field(..., alias="1")
    typing_type: TypingMode = Field(..., alias="2")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            typing_type: TypingMode,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                peer=peer,
                typing_type=typing_type,
                **__pydantic_kwargs
            )
