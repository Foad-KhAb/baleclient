from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types import InfoPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class UnblockUser(BaleMethod):
    __service__ = Services.USER.value
    __method__ = "UnblockUser"

    __returning__ = DefaultResponse

    peer: InfoPeer = Field(..., alias="1")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, peer: InfoPeer, **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(peer=peer, **__pydantic_kwargs)
