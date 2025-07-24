import time
from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class EditUserLocalName(BaleMethod):
    __service__ = Services.USER.value
    __method__ = "EditUserLocalName"

    __returning__ = DefaultResponse

    user_id: int = Field(..., alias="1")
    access_hash: int = Field(..., alias="2")
    name: str = Field(..., alias="3")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            user_id: int,
            name: str,
            access_hash: int,
            **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(
                name=name, user_id=user_id, access_hash=access_hash, **__pydantic_kwargs
            )
