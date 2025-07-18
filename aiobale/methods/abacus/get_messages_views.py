from pydantic import Field
from typing import TYPE_CHECKING, List

from ...types import Peer, OtherMessage
from ...types.responses import ViewsResponse
from ...enums import Services
from ..base import BaleMethod


class GetMessagesViews(BaleMethod):
    __service__ = Services.ABACUS.value
    __method__ = "GetMessagesViews"
    
    __returning__ = ViewsResponse
    
    peer: Peer = Field(..., alias="1")
    message_ids: List[OtherMessage] = Field(..., alias="2")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message_ids: List[OtherMessage],
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                peer=peer,
                message_ids=message_ids,
                **__pydantic_kwargs
            )
