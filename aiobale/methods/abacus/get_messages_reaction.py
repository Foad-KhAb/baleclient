from pydantic import Field
from typing import TYPE_CHECKING, List

from ...types import Peer, OtherMessage
from ...types.responses import ReactionsResponse
from ...enums import Services
from ..base import BaleMethod


class GetMessagesReactions(BaleMethod):
    __service__ = Services.ABACUS.value
    __method__ = "GetMessagesReactions"

    __returning__ = ReactionsResponse

    peer: Peer = Field(..., alias="1")
    message_ids: List[OtherMessage] = Field(..., alias="2")

    origin_peer: Peer = Field(..., alias="3")
    origin_message_ids: List[OtherMessage] = Field(..., alias="4")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            message_ids: List[OtherMessage],
            origin_peer: Peer,
            origin_message_ids: List[OtherMessage],
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                peer=peer,
                message_ids=message_ids,
                origin_peer=origin_peer,
                origin_message_ids=origin_message_ids,
                **__pydantic_kwargs
            )
