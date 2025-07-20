from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer, Condition
from ...types.responses import FullGroupResponse
from ...enums import Services
from ..base import BaleMethod


class LoadMembers(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "LoadMembers"
    
    __returning__ = FullGroupResponse
    
    group: ShortPeer = Field(..., alias="1")
    limit: int = Field(..., alias="2")
    next: Optional[int] = Field(None, alias="3")
    condition: Optional[Condition] = Field(None, alias="4")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            limit: int,
            next: int,
            condition: Optional[Condition] = None,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                group=group,
                limit=limit,
                next=next,
                condition=condition,
                **__pydantic_kwargs
            )
