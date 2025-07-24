from pydantic import Field
from typing import TYPE_CHECKING

from ...types import ShortPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class EditChannelUsername(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "EditChannelNick"

    __returning__ = DefaultResponse

    group: ShortPeer = Field(..., alias="1")
    username: str = Field(..., alias="2")
    random_id: int = Field(..., alias="3")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            username: str,
            random_id: int,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                random_id=random_id, group=group, username=username, **__pydantic_kwargs
            )
