from pydantic import model_validator
from typing import Optional, Any, Dict

from .default import DefaultResponse
from ...types import Message, PrevMessage
from ...client.client import Client
from ...methods import SendMessage


class MessageResponse(DefaultResponse):
    message: Optional[Message]

    @model_validator(mode="before")
    @classmethod
    def add_message(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "message" in data:
            return data

        client: Client = data.get("client_cls")
        method: SendMessage = data.get("method_data")
        ext_fields = data.get("ext", [])

        prev_data = {
            "message_id": field.value.number
            for field in ext_fields
            if field.name == "previous_message_rid"
        }
        prev_data.update({
            "date": field.value.number
            for field in ext_fields
            if field.name == "previous_message_date"
        })

        prev_message = PrevMessage.model_validate(prev_data) if prev_data else None

        data["message"] = Message(
            chat=method.chat,
            sender_id=client.id,
            data=data.get("date"),
            message_id=method.message_id,
            content=method.content,
            previous_message=prev_message
        )

        return data
