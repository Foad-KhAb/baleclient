from pydantic import Field, model_validator
from typing import TYPE_CHECKING, Any, Dict, List

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

    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes the 'data' field (alias '1') to always be a list.
        """
        if "1" in data and not isinstance(data["1"], list):
            data["1"] = [data["1"]]

        return data
