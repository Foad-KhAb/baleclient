from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types import Peer
from ...types.responses import HistoryResponse
from ...enums import Services
from ..base import BaleMethod


class LoadPinnedMessages(BaleMethod):
    __service__ = Services.MESSAGING.value
    __method__ = "LoadPinnedMessages"

    __returning__ = HistoryResponse

    peer: Peer = Field(..., alias="1")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, peer: Peer, **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(peer=peer, **__pydantic_kwargs)
