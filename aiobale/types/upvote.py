from pydantic import Field
from typing import TYPE_CHECKING, List

from .base import BaleObject
from ..types import InfoMessage


class Upvote(BaleObject):
    messages: List[InfoMessage] = Field(..., alias="1")
    limit: int = Field(..., alias="2")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            message: List[InfoMessage],
            limit: int,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(message=message, limit=limit, **__pydantic_kwargs)
