from pydantic import Field
from typing import TYPE_CHECKING

from ...types import ShortPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class RemoveUserAdmin(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "RemoveUserAdmin"
    
    __returning__ = DefaultResponse
    
    group: ShortPeer = Field(..., alias="1")
    user: ShortPeer = Field(..., alias="2")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            user: ShortPeer,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                group=group,
                user=user,
                **__pydantic_kwargs
            )
