from pydantic import Field
from typing import TYPE_CHECKING, Any, List

from ...types.responses import ContactsResponse
from ...types import ContactData
from ...enums import Services
from ..base import BaleMethod


class ImportContacts(BaleMethod):
    __service__ = Services.USER.value
    __method__ = "ImportContacts"
    
    __returning__ = ContactsResponse
    
    phones: List[ContactData] = Field(..., alias="1")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            phones: List[ContactData],
            **__pydantic_kwargs: Any
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                phones=phones,
                **__pydantic_kwargs
            )
