from pydantic import Field
from typing import TYPE_CHECKING

from ...types.responses import FullGroupResponse
from ...enums import Services
from ..base import BaleMethod


class GetGroupPreview(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "GetGroupPreview"

    __returning__ = FullGroupResponse

    token: str = Field(..., alias="1")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(__pydantic__self__, *, token: str, **__pydantic_kwargs) -> None:
            super().__init__(token=token, **__pydantic_kwargs)
