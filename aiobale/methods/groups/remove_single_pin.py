from pydantic import Field
from typing import TYPE_CHECKING

from ...types import ShortPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class RemoveSinglePin(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "RemoveSinglePin"
    
    __returning__ = DefaultResponse
    
    group: ShortPeer = Field(..., alias="1")
    message_id: int = Field(..., alias="2")
    date: int = Field(..., alias="3")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            message_id: int,
            date: int,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                group=group,
                date=date,
                message_id=message_id,
                **__pydantic_kwargs
            )
