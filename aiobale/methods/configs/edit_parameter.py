from pydantic import Field
from typing import TYPE_CHECKING

from ...types.responses import DefaultResponse
from ...types import StringValue
from ...enums import Services
from ..base import BaleMethod


class EditParameter(BaleMethod):
    __service__ = Services.CONFIGS.value
    __method__ = "EditParameter"

    __returning__ = DefaultResponse

    key: str = Field(..., alias="1")
    value: StringValue = Field(..., alias="2")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, key: str, value: StringValue, **__pydantic_kwargs
        ) -> None:
            super().__init__(key=key, value=value, **__pydantic_kwargs)
