from pydantic import Field
from typing import TYPE_CHECKING, Any, List

from ...types import InfoPeer
from ...types.responses import FullUsersResponse
from ...enums import Services
from ..base import BaleMethod


class LoadFullUsers(BaleMethod):
    __service__ = Services.USER.value
    __method__ = "LoadFullUsers"
    
    __returning__ = FullUsersResponse
    
    peers: List[InfoPeer] = Field(..., alias="1")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            peers: List[InfoPeer],
            **__pydantic_kwargs: Any
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                peers=peers,
                **__pydantic_kwargs
            )
