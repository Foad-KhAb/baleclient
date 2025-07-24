from pydantic import Field
from typing import TYPE_CHECKING

from ...types import Peer
from ...types.responses import DefaultResponse
from ...enums import Services, TypingMode
from ..base import BaleMethod


class Typing(BaleMethod):
    __service__ = Services.PRESENCE.value
    __method__ = "Typing"

    __returning__ = DefaultResponse

    peer: Peer = Field(..., alias="1")
    typing_type: TypingMode = Field(..., alias="2")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            typing_type: TypingMode,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(peer=peer, typing_type=typing_type, **__pydantic_kwargs)
