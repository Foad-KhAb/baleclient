from pydantic import Field, model_validator
from typing import TYPE_CHECKING, Any, Dict, List

from ...types import Peer, IntValue, BytesValue, InfoMessage
from ...utils import Int64VarintCodec
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class ForwardMessages(BaleMethod):
    __service__ = Services.MESSAGING.value
    __method__ = "ForwardMessages"
    
    __returning__ = DefaultResponse
    
    peer: Peer = Field(..., alias="1")
    message_ids: bytes = Field(..., alias="2")
    forwarded_messages: List[InfoMessage] = Field(..., alias="3")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message_ids: List[int],
            forwarded_messages: List[InfoMessage],
            **__pydantic_kwargs: Any
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                peer=peer,
                message_ids=message_ids,
                forwarded_messages=forwarded_messages
                **__pydantic_kwargs
            )
            
    @model_validator(mode="before")
    @classmethod
    def fix_lists(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["message_ids"] = Int64VarintCodec.encode_list(data["message_ids"])
        return data
