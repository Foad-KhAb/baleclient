from pydantic import Field
from typing import TYPE_CHECKING, List

from ...types import ShortPeer
from ...types.responses import FullGroupResponse
from ...enums import Services
from ..base import BaleMethod


class GetFullGroup(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "GetFullGroup"

    __returning__ = FullGroupResponse

    group: ShortPeer = Field(..., alias="1")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, group: ShortPeer, **__pydantic_kwargs
        ) -> None:
            super().__init__(group=group, **__pydantic_kwargs)
