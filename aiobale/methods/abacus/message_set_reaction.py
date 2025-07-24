from pydantic import Field
from typing import TYPE_CHECKING

from ...types import Peer
from ...types.responses import ReactionSentResponse
from ...enums import Services
from ..base import BaleMethod


class MessageSetReaction(BaleMethod):
    __service__ = Services.ABACUS.value
    __method__ = "MessageSetReaction"

    __returning__ = ReactionSentResponse

    peer: Peer = Field(..., alias="1")
    message_id: int = Field(..., alias="2")
    emojy: str = Field(..., alias="3")
    date: int = Field(..., alias="4")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message_id: int,
            date: int,
            emojy: str,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                peer=peer,
                message_id=message_id,
                date=date,
                emojy=emojy,
                **__pydantic_kwargs
            )
