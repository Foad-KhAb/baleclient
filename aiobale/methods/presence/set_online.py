from pydantic import Field
from typing import TYPE_CHECKING

from ...types import IntBool
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class SetOnline(BaleMethod):
    __service__ = Services.PRESENCE.value
    __method__ = "SetOnline"
    
    __returning__ = DefaultResponse
    
    is_online: IntBool = Field(..., alias="1")
    timeout: int = Field(..., alias="2")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            is_online: bool,
            timeout: int,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                is_online=is_online,
                timeout=timeout,
                **__pydantic_kwargs
            )
