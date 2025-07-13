from pydantic import Field
from typing import TYPE_CHECKING, Any, List

from ...types import Peer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class LoadFullUsers(BaleMethod):
    __service__ = Services.USER.value
    __method__ = "LoadFullUsers"
    
    __returning__ = DefaultResponse
    
    peers: List[Peer] = Field(..., alias="1")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            peers: str,
            **__pydantic_kwargs: Any
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                peers=peers,
                **__pydantic_kwargs
            )
