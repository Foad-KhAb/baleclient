from pydantic import Field
from typing import TYPE_CHECKING, Any, List

from ...types import Peer, OtherMessage, IntBool
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class UnPinMessages(BaleMethod):
    __service__ = Services.MESSAGING.value
    __method__ = "UnPinMessages"

    __returning__ = DefaultResponse

    peer: Peer = Field(..., alias="1")
    messages: List[OtherMessage] = Field(..., alias="2")
    all_messages: IntBool = Field(False, alias="3")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            messages: List[OtherMessage],
            all_messages: IntBool = False,
            **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(
                peer=peer,
                messages=messages,
                all_messages=all_messages,
                **__pydantic_kwargs
            )
