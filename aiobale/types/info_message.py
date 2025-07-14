from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING, Any, Optional, Union

from .peer import Peer
from .base import BaleObject
from .values import IntValue
from .other_message import OtherMessage


class InfoMessage(BaleObject):
    peer: Peer = Field(..., alias="1")
    message_id: int = Field(..., alias="2")
    date: Union[IntValue, int] = Field(..., alias="3")
    previous_message: Optional[OtherMessage] = Field(None, alias="4")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            self,
            *,
            peer: Peer,
            message_id: int,
            date: IntValue,
            **__pydantic_kwargs: Any
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                peer=peer,
                message_id=message_id,
                date=date,
                **__pydantic_kwargs
            )
