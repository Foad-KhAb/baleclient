from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer, StringValue
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class EditGroupAbout(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "EditGroupAbout"
    
    __returning__ = DefaultResponse
    
    group: ShortPeer = Field(..., alias="1")
    random_id: int = Field(..., alias="2")
    about: StringValue = Field(..., alias="3")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            random_id: int,
            about: StringValue,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                random_id=random_id,
                group=group,
                about=about,
                **__pydantic_kwargs
            )
