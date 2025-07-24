from pydantic import Field
from typing import TYPE_CHECKING, Any, Optional

from ...types import Peer, MessageContent
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class DeleteChat(BaleMethod):
    __service__ = Services.MESSAGING.value
    __method__ = "DeleteChat"

    __returning__ = DefaultResponse

    peer: Peer = Field(..., alias="1")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(__pydantic__self__, *, peer: Peer, **__pydantic_kwargs) -> None:
            super().__init__(peer=peer, **__pydantic_kwargs)
