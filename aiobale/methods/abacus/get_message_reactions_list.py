from pydantic import Field
from typing import TYPE_CHECKING, List

from ...types import Peer, OtherMessage
from ...types.responses import ReactionListResponse
from ...enums import Services
from ..base import BaleMethod


class GetMessageReactionsList(BaleMethod):
    __service__ = Services.ABACUS.value
    __method__ = "GetMessageReactionsList"
    
    __returning__ = ReactionListResponse
    
    peer: Peer = Field(..., alias="1")
    message_id: int = Field(..., alias="2")
    date: int = Field(..., alias="3")
    emojy: str = Field(..., alias="4")
    page: int = Field(..., alias="5")
    limit: int = Field(..., alias="6")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message_id: int,
            date: int,
            emojy: str,
            page: int,
            limit: int,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                peer=peer,
                message_id=message_id,
                date=date,
                emojy=emojy,
                page=page,
                limit=limit,
                **__pydantic_kwargs
            )
