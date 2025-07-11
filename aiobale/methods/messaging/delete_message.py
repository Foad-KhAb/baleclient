from pydantic import Field, model_validator
from typing import TYPE_CHECKING, Any, Dict, List

from ...types import Peer, IntValue, BytesValue
from ...utils import Int64VarintCodec
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class DeleteMessage(BaleMethod):
    __service__ = Services.MESSAGING.value
    __method__ = "DeleteMessage"
    
    __returning__ = DefaultResponse
    
    peer: Peer = Field(..., alias="1")
    message_ids: bytes = Field(..., alias="2")
    dates: BytesValue = Field(..., alias="3")
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
            
    @model_validator(mode="before")
    @classmethod
    def fix_lists(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["message_ids"] = Int64VarintCodec.encode_list(data["message_ids"])
        data["dates"] = BytesValue(
            value=Int64VarintCodec.encode_list(data["dates"])
        )
        
        return data
