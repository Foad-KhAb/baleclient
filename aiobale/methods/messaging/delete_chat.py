from pydantic import Field
from typing import TYPE_CHECKING, Any, Optional

from ...types import Peer, MessageContent
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class DeleteChat(BaleMethod):
    __service__ = Services.MESSAGING.value
    __method__ = "DeleteChat"
    
    __returning__ = DefaultResponse
    
    peer: Peer = Field(..., alias="1")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                peer=peer,
                **__pydantic_kwargs
            )
