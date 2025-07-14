from pydantic import Field
from typing import TYPE_CHECKING, Any, List

from ...types.responses import ContactsResponse
from ...types import ContactData
from ...enums import Services
from ..base import BaleMethod


class RemoveContact(BaleMethod):
    __service__ = Services.USER.value
    __method__ = "RemoveContact"
    
    __returning__ = ContactsResponse
    
    user_id: int = Field(..., alias="1")
    type: int = Field(1, alias="2")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            user_id: int,
            type: int = 1,
            **__pydantic_kwargs: Any
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                user_id=user_id,
                type=type,
                **__pydantic_kwargs
            )
