from __future__ import annotations

from pydantic import ValidationInfo, model_validator
from typing import Optional, Any, Dict, TYPE_CHECKING

from .default import DefaultResponse
from ...types import Message, OtherMessage, ExtData

if TYPE_CHECKING:
    from ...methods import SendMessage


class MessageResponse(DefaultResponse):
    message: Optional[Message]

    @model_validator(mode="before")
    @classmethod
    def add_message(cls, data: Dict[str, Any], info: ValidationInfo) -> Dict[str, Any]:
        if "message" in data:
            return data

        client = info.context.get("client")
        if client is None:
            raise ValueError("client not found in context")

        method: SendMessage = data.get("method_data")
        exts = [ExtData.model_validate(value) for value in data.get("4", [])]

        prev_data = {
            "message_id": field.value.number
            for field in exts
            if field.name == "previous_message_rid"
        }
        prev_data.update({
            "date": field.value.number
            for field in exts
            if field.name == "previous_message_date"
        })

        prev_message = OtherMessage.model_validate(prev_data) if prev_data else None
        
        if hasattr(method.content, "document") and getattr(method.content.document, "thumb", None):
            thumb = method.content.document.thumb
            if isinstance(thumb.image, bytes):
                thumb.image = thumb.image.hex()

        data["message"] = Message(
            chat=method.chat,
            sender_id=client.id,
            date=data.get("2", 0),
            message_id=method.message_id,
            content=method.content,
            previous_message=prev_message
        ).as_(client)

        return data
