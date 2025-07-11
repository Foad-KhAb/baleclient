from __future__ import annotations

from pydantic import Field
from typing import Optional

from .base import BaleObject


class TextMessage(BaleObject):
    value: str = Field(..., alias="1")
    

class MessageCaption(BaleObject):
    content: Optional[str] = Field(None, alias="1")
    mentions: Optional[list | dict] = Field({}, alias="2")
    ext: Optional[dict] = Field({}, alias="3")
    

class DocumentMessage(BaleObject):
    file_id: int = Field(..., alias="1")
    access_hash: int = Field(..., alias="2")
    file_size: int = Field(..., alias="3")
    name: str = Field(..., alias="4")
    mime_type: str = Field(..., alias="5")
    ext: dict = Field(..., alias="7")
    caption: MessageCaption = Field(..., alias="8")


class MessageContent(BaleObject):
    document: Optional[DocumentMessage] = Field(None, alias="4")
    text: Optional[TextMessage] = Field(None, alias="15")    
