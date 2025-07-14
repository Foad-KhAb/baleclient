from typing import Optional
from pydantic import Field, model_validator

from ..enums import ChatType
from .base import BaleObject
from .message_data import MessageData
from .message import Message
from .other_message import OtherMessage
from .chat import Chat


class GroupMessagePinned(BaleObject):
    group_id: int = Field(..., alias="1")
    message_data: MessageData = Field(..., alias="2")
    
    message: Optional[Message] = Field(None, exclude=None)
    
    @model_validator(mode="after")
    def validate(self):
        chat = Chat(id=self.group_id, type=ChatType.GROUP)
        self.message_data.chat = chat
        
        if self.message_data.replied_to is not None:
            self.message_data.replied_to.chat = chat
        
        # Prevent infinite loop: bypass Pydantic
        object.__setattr__(self, "message", self.message_data.message)
        return self


class GroupPinRemoved(BaleObject):
    group_id: int = Field(..., alias="1")
    message: OtherMessage  = Field(..., alias="2")
