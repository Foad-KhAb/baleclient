from pydantic import Field
from typing import TYPE_CHECKING

from ...types import Peer
from ...types.responses import JoinedGroupResponse
from ...enums import Services
from ..base import BaleMethod


class JoinPublicGroup(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "JoinPublicGroup"
    
    __returning__ = JoinedGroupResponse
    
    peer: Peer = Field(..., alias="1")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                peer=peer,
                **__pydantic_kwargs
            )
