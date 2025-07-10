import time
from pydantic import Field
from typing import TYPE_CHECKING, Any

from ..types.responses import NickNameAvailable
from ..enums import Services
from .base import BaleMethod


class CheckNickName(BaleMethod):
    __service__ = Services.USER.value
    __method__ = "CheckNickName"
    
    __returning__ = NickNameAvailable
    
    nick_name: str = Field(..., alias="1")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            nick_name: str,
            **__pydantic_kwargs: Any
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                nick_name=nick_name,
                **__pydantic_kwargs
            )
