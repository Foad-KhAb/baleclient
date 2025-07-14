from pydantic import Field
from typing import TYPE_CHECKING, Any, List

from ...types import InfoPeer
from ...types.responses import UsersResponse
from ...enums import Services
from ..base import BaleMethod


class UnblockUser(BaleMethod):
    __service__ = Services.USER.value
    __method__ = "UnblockUser"
    
    __returning__ = UsersResponse
    
    peer: InfoPeer = Field(..., alias="1")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            peer: InfoPeer,
            **__pydantic_kwargs: Any
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                peer=peer,
                **__pydantic_kwargs
            )
