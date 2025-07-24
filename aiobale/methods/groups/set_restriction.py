from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer, StringValue
from ...types.responses import DefaultResponse
from ...enums import Services, Restriction
from ..base import BaleMethod


class SetRestriction(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "SetRestriction"

    __returning__ = DefaultResponse

    group: ShortPeer = Field(..., alias="1")
    restriction: Restriction = Field(..., alias="2")
    username: Optional[StringValue] = Field(None, alias="3")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            restriction: Restriction,
            username: Optional[StringValue] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                group=group,
                restriction=restriction,
                username=username,
                **__pydantic_kwargs
            )
