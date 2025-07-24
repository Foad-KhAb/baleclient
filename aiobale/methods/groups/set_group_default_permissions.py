from pydantic import Field
from typing import TYPE_CHECKING

from ...types import ShortPeer, Permissions
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class SetGroupDefaultPermissions(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "SetGroupDefaultPermissions"

    __returning__ = DefaultResponse

    group: ShortPeer = Field(..., alias="1")
    permissions: Permissions = Field(..., alias="2")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            permissions: Permissions,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(group=group, permissions=permissions, **__pydantic_kwargs)
