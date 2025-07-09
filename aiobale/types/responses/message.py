from __future__ import annotations

from pydantic import model_validator
from typing import Optional, Any, Dict, TYPE_CHECKING

from .default import DefaultResponse

if TYPE_CHECKING:
    from ...types import Message, PrevMessage, ExtData
    from ...methods import SendMessage
    from ...client.client import Client


class MessageResponse(DefaultResponse):
    message: Optional["Message"]

    @model_validator(mode="before")
    @classmethod
    def add_message(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "message" in data:
            return data

        client: Client = data.get("client_cls")
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

        prev_message = PrevMessage.model_validate(prev_data) if prev_data else None

        data["message"] = Message(
            chat=method.chat,
            sender_id=client.id,
            date=data.get("2", 0),
            message_id=method.message_id,
            content=method.content,
            previous_message=prev_message
        )
        return data
