from pydantic import Field
from typing import TYPE_CHECKING, Any, Optional

from ..types.responses import ValidateCodeResponse
from ..enums import Services
from .base import BaleMethod


class ValidateCode(BaleMethod):
    __service__ = Services.AUTH.value
    __method__ = "ValidateCode"
    
    __returning__ = None

    transaction_hash: str = Field(..., alias="1")
    code: str = Field(..., alias="2")
    is_jwt: Optional[dict] = Field(default_factory=lambda: {"1": 1}, alias="3")

    # This __init__ is only for type hinting and IDE autocomplete.
    if TYPE_CHECKING:
        def __init__(
            self,
            *,
            transaction_hash: str,
            code: str,
            **kwargs: Any,
        ) -> None:
            super().__init__(
                transaction_hash=transaction_hash,
                code=code
                **kwargs,
            )
