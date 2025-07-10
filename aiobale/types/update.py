from functools import cached_property
from pydantic import Field
from typing import Any, Optional, Tuple

from .base import BaleObject
from .message import Message


class Update(BaleObject):
    message: Optional[Message] = Field(None, alias="55")
    
    @cached_property
    def current_event(self) -> Optional[Tuple[str, Any]]:
        for field_name in self.__annotations__:
            value = getattr(self, field_name, None)
            if value is not None:
                return field_name, value
        return None


class UpdateBody(BaleObject):
    body: Optional[Update] = Field(None, alias="1")
    update_id: Optional[int] = Field(..., alias="3")
    date: int = Field(..., alias="4")
