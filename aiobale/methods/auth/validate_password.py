from pydantic import Field
from typing import TYPE_CHECKING, Any, Optional

from ...enums import Services
from ..base import BaleMethod


class ValidatePassword(BaleMethod):
    __service__ = Services.AUTH.value
    __method__ = "ValidatePassword"
    
    __returning__ = None

    transaction_hash: str = Field(..., alias="1")
    password: str = Field(..., alias="2")
    is_jwt: Optional[dict] = Field(default_factory=lambda: {"1": 1}, alias="3")

    # This __init__ is only for type hinting and IDE autocomplete.
    if TYPE_CHECKING:
        def __init__(
            self,
            *,
            transaction_hash: str,
            password: str,
            **kwargs: Any,
        ) -> None:
            super().__init__(
                transaction_hash=transaction_hash,
                password=password
                **kwargs,
            )
