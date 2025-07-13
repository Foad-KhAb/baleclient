from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types import Peer
from ...types.responses import HistoryResponse
from ...enums import Services
from ..base import BaleMethod


class LoadDialogs(BaleMethod):
    __service__ = Services.MESSAGING.value
    __method__ = "LoadDialogs"
    
    __returning__ = HistoryResponse
    
    offset_date: int = Field(..., alias="1")
    limit: int = Field(..., alias="2")
    exclute_pinned: bool = Field(..., alias="5")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            offset_date: int,
            limit: int,
            exclude_pinned: bool,
            **__pydantic_kwargs: Any
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                offset_date=offset_date,
                limit=limit,
                exclude_pinned=exclude_pinned,
                **__pydantic_kwargs
            )
