from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer
from ...types.responses import InviteResponse
from ...enums import Services
from ..base import BaleMethod


class InviteUsers(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "InviteUsers"
    
    __returning__ = InviteResponse
    
    group: ShortPeer = Field(..., alias="1")
    random_id: int = Field(..., alias="2")
    users: List[ShortPeer] = Field(..., alias="3")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            random_id: int,
            users: List[ShortPeer],
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                random_id=random_id,
                group=group,
                users=users,
                **__pydantic_kwargs
            )
