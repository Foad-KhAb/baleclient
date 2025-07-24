from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class TransferOwnership(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "TransferOwnership"

    __returning__ = DefaultResponse

    group: ShortPeer = Field(..., alias="1")
    new_owner: int = Field(..., alias="2")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, group: ShortPeer, new_owner: int, **__pydantic_kwargs
        ) -> None:
            super().__init__(group=group, new_owner=new_owner, **__pydantic_kwargs)
