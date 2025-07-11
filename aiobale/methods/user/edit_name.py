import time
from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types import Peer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class EditName(BaleMethod):
    __service__ = Services.USER.value
    __method__ = "EditName"
    
    __returning__ = DefaultResponse
    
    name: str = Field(..., alias="1")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            name: str,
            **__pydantic_kwargs: Any
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                name=name,
                **__pydantic_kwargs
            )
