from typing import TYPE_CHECKING, Any, Optional
from pydantic import Field

from ..enums import ChatType
from .base import BaleObject


class InfoPeer(BaleObject):
    id: int = Field(..., alias="1")
    type: Optional[ChatType] = Field(None, alias="2")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            id: int,
            type: Optional[ChatType] = None,
            **__pydantic_kwargs: Any
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                id=id,
                type=type,
                **__pydantic_kwargs
            )
