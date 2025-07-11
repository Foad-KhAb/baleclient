from functools import cached_property
from pydantic import Field
from typing import Any, Optional, Tuple

from .base import BaleObject
from .message import Message
from .selected_messages import SelectedMessages
from .chat_data import ChatData
from .username_changed import UsernameChanged
from .info_message import InfoMessage


class Update(BaleObject):
    message_sent: Optional[InfoMessage] = Field(None, alias="4")
    message_deleted: Optional[SelectedMessages] = Field(None, alias="46")
    chat_cleared: Optional[ChatData] = Field(None, alias="47")
    chat_deleted: Optional[ChatData] = Field(None, alias="48")
    message: Optional[Message] = Field(None, alias="55")
    username_changed: Optional[UsernameChanged] = Field(None, alias="209")
    
    @cached_property
    def current_event(self) -> Optional[Tuple[str, Any]]:
        for field_name in self.__annotations__:
            value = getattr(self, field_name, None)
            if value is not None:
                return field_name, value
        return None


class UpdateBody(BaleObject):
    body: Optional[Update] = Field(None, alias="1")
    update_id: Optional[int] = Field(None, alias="3")
    date: int = Field(..., alias="4")
