from pydantic import Field
from typing import TYPE_CHECKING

from ...types import InfoMessage, StringValue
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class GetMessageUpvoters(BaleMethod):
    __service__ = Services.MAGAZINE.value
    __method__ = "GetMessageUpvoters"

    __returning__ = DefaultResponse

    load_more_state: StringValue = Field(..., alias="1")
    message: InfoMessage = Field(..., alias="2")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            load_more_state: StringValue,
            message: InfoMessage,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                message=message, load_more_state=load_more_state, **__pydantic_kwargs
            )
