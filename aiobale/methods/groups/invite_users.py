from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer
from ...types.responses import InviteResponse
from ...enums import Services
from ..base import BaleMethod


class InviteUsers(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "InviteUsers"

    __returning__ = InviteResponse

    group: ShortPeer = Field(..., alias="1")
    random_id: int = Field(..., alias="2")
    users: List[ShortPeer] = Field(..., alias="3")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            random_id: int,
            users: List[ShortPeer],
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                random_id=random_id, group=group, users=users, **__pydantic_kwargs
            )
