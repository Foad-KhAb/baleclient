from pydantic import Field
from typing import TYPE_CHECKING

from ...types.responses import JoinedGroupResponse
from ...enums import Services
from ..base import BaleMethod


class JoinGroup(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "JoinGroup"
    
    __returning__ = JoinedGroupResponse
    
    token: str = Field(..., alias="1")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            token: str,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                token=token,
                **__pydantic_kwargs
            )
