from pydantic import Field
from typing import TYPE_CHECKING, Optional

from ...types import ShortPeer, StringValue
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class MakeUserAdmin(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "MakeUserAdmin"
    
    __returning__ = DefaultResponse
    
    group: ShortPeer = Field(..., alias="1")
    user: ShortPeer = Field(..., alias="2")
    admin_name: Optional[StringValue] = Field(None, alias="3")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            user: ShortPeer,
            admin_name: Optional[str] = None,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                group=group,
                user=user,
                admin_name=admin_name,
                **__pydantic_kwargs
            )
