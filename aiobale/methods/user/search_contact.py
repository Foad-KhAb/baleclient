from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types.responses import ContactResponse
from ...enums import Services
from ..base import BaleMethod


class SearchContact(BaleMethod):
    __service__ = Services.USER.value
    __method__ = "SearchContacts"

    __returning__ = ContactResponse

    request: str = Field(..., alias="1")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, request: str, **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(request=request, **__pydantic_kwargs)
