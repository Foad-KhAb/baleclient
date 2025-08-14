from pydantic import Field
from typing import TYPE_CHECKING, Optional

from ...types import InfoMessage, IntValue
from ...types.responses import UpvoteResponse
from ...enums import Services
from ..base import BaleMethod


class UpvotePost(BaleMethod):
    __service__ = Services.MAGAZINE.value
    __method__ = "UpvotePost"

    __returning__ = UpvoteResponse

    message: InfoMessage = Field(..., alias="1")
    album_id: Optional[IntValue] = Field(None, alias="2")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            message: InfoMessage,
            album_id: Optional[IntValue] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(message=message, album_id=album_id, **__pydantic_kwargs)
