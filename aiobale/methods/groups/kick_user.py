from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class KickUser(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "KickUser"
    
    __returning__ = DefaultResponse
    
    group: ShortPeer = Field(..., alias="1")
    random_id: int = Field(..., alias="2")
    user: ShortPeer = Field(..., alias="3")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            random_id: int,
            user: ShortPeer,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                group=group,
                random_id=random_id,
                user=user,
                **__pydantic_kwargs
            )
