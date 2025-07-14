from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types.responses import ContactResponse
from ...enums import Services
from ..base import BaleMethod


class SearchContact(BaleMethod):
    __service__ = Services.USER.value
    __method__ = "SearchContacts"
    
    __returning__ = ContactResponse
    
    requst: str = Field(..., alias="1")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            request: str,
            **__pydantic_kwargs: Any
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                request=request,
                **__pydantic_kwargs
            )
