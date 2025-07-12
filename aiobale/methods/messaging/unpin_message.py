from pydantic import Field, model_validator
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ...types import Peer, InfoMessage, OtherMessage, IntBool
from ...utils import Int64VarintCodec
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class UnPinMessages(BaleMethod):
    __service__ = Services.MESSAGING.value
    __method__ = "UnPinMessages"
    
    __returning__ = DefaultResponse
    
    peer: Peer = Field(..., alias="1")
    messages: List[OtherMessage] = Field(..., alias="2")
    all_messages: Optional[IntBool] = Field(None, alias="3")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            messages: List[OtherMessage],
            all_messages: Optional[IntBool] = None,
            **__pydantic_kwargs: Any
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                peer=peer,
                messages=messages,
                all_messages=all_messages,
                **__pydantic_kwargs
            )
