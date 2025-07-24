from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class EditGroupTitle(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "EditGroupTitle"

    __returning__ = DefaultResponse

    group: ShortPeer = Field(..., alias="1")
    random_id: int = Field(..., alias="4")
    title: str = Field(..., alias="3")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            random_id: int,
            title: str,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                random_id=random_id, group=group, title=title, **__pydantic_kwargs
            )
