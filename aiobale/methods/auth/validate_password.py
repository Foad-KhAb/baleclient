from pydantic import Field
from typing import TYPE_CHECKING, Optional

from ...enums import Services
from ..base import BaleMethod


class ValidatePassword(BaleMethod):
    __service__ = Services.AUTH.value
    __method__ = "ValidatePassword"
    
    __returning__ = None

    transaction_hash: str = Field(..., alias="1")
    password: str = Field(..., alias="2")
    is_jwt: Optional[dict] = Field(default_factory=lambda: {"1": 1}, alias="3")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            self,
            *,
            transaction_hash: str,
            password: str,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                transaction_hash=transaction_hash,
                password=password,
                **__pydantic_kwargs
            )
