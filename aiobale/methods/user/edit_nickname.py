import time
from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types.responses import DefaultResponse
from ...types import StringValue
from ...enums import Services
from ..base import BaleMethod


class EditNickName(BaleMethod):
    __service__ = Services.USER.value
    __method__ = "EditNickName"

    __returning__ = DefaultResponse

    nick_name: StringValue = Field(..., alias="1")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, nick_name: StringValue, **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(nick_name=nick_name, **__pydantic_kwargs)
