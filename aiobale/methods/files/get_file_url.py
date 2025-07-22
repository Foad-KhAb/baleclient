from pydantic import Field
from typing import TYPE_CHECKING

from ...types import FileInfo
from ...types.responses import FileURLResponse
from ...enums import Services
from ..base import BaleMethod


class GetFileUrl(BaleMethod):
    __service__ = Services.FILES.value
    __method__ = "GetNasimFileUrl"
    
    __returning__ = FileURLResponse
    
    file: FileInfo = Field(..., alias="1")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            file: FileInfo,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                file=file,
                **__pydantic_kwargs
            )
