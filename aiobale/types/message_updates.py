from typing import Optional
from pydantic import Field, model_validator

from .base import BaleObject
from .message_data import MessageData
from .message import Message
from .other_message import OtherMessage


class GroupMessagePinned(BaleObject):
    group_id: int = Field(..., alias="1")
    message_data: MessageData = Field(..., alias="2")
    
    message: Optional[Message] = None
    
    @model_validator(mode="after")
    def validate(self):
        self.message = self.message_data.message
        return self


class GroupPinRemoved(BaleObject):
    group_id: int = Field(..., alias="1")
    message: OtherMessage  = Field(..., alias="2")
