from pydantic import Field
from typing import TYPE_CHECKING

from ...types.responses import ParametersResponse
from ...types import StringValue
from ...enums import Services
from ..base import BaleMethod


class EditParameter(BaleMethod):
    __service__ = Services.CONFIGS.value
    __method__ = "EditParameter"
    
    __returning__ = ParametersResponse
    
    key: str = Field(..., alias="1")
    value: StringValue = Field(..., alias="2")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            key: str,
            value: StringValue,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                key=key,
                value=value,
                **__pydantic_kwargs
            )
