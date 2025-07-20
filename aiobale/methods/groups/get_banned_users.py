from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer
from ...types.responses import BannedUsersResponse
from ...enums import Services
from ..base import BaleMethod


class GetBannedUsers(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "GetBannedUsers"
    
    __returning__ = BannedUsersResponse
    
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
