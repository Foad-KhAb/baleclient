from pydantic import Field
from typing import TYPE_CHECKING

from ...types import InfoMessage, IntValue
from ...types.responses import UpvoteResponse
from ...enums import Services
from ..base import BaleMethod


class RevokeUpvotedPost(BaleMethod):
    __service__ = Services.MAGAZINE.value
    __method__ = "RevokeUpvotedPost"

    __returning__ = UpvoteResponse

    message: InfoMessage = Field(..., alias="1")
    album_id: IntValue = Field(..., alias="2")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            message: InfoMessage,
            album_id: IntValue,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(message=message, album_id=album_id, **__pydantic_kwargs)
