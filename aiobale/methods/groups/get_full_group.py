from pydantic import Field
from typing import TYPE_CHECKING, List

from ...types import ShortPeer
from ...types.responses import FullGroupResponse
from ...enums import Services
from ..base import BaleMethod


class GetFullGroup(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "GetFullGroup"
    
    __returning__ = FullGroupResponse
    
    group: ShortPeer = Field(..., alias="1")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                group=group,
                **__pydantic_kwargs
            )
