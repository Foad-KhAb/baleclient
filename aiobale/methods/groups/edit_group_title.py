from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class EditGroupTitle(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "EditGroupTitle"
    
    __returning__ = DefaultResponse
    
    group: ShortPeer = Field(..., alias="1")
    random_id: int = Field(..., alias="4")
    title: str = Field(..., alias="3")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            random_id: int,
            title: str,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                random_id=random_id,
                group=group,
                title=title,
                **__pydantic_kwargs
            )
