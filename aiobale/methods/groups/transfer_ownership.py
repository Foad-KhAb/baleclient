from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class TransferOwnership(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "TransferOwnership"
    
    __returning__ = DefaultResponse
    
    group: ShortPeer = Field(..., alias="1")
    new_owner: int = Field(..., alias="2")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            new_owner: int,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                group=group,
                new_owner=new_owner,
                **__pydantic_kwargs
            )
