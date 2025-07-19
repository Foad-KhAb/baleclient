from pydantic import Field
from typing import TYPE_CHECKING

from ...types import ShortPeer
from ...types.responses import GetPinsResponse
from ...enums import Services
from ..base import BaleMethod


class GetPins(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "GetPins"
    
    __returning__ = GetPinsResponse
    
    group: ShortPeer = Field(..., alias="1")
    page: int = Field(..., alias="2")
    limit: int = Field(..., alias="3")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            page: int,
            limit: int,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                group=group,
                page=page,
                limit=limit,
                **__pydantic_kwargs
            )
