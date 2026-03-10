from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field, model_validator

from .base import BaleObject


class OtherMessage(BaleObject):
    """
    Represents a reference to another message within the Bale platform.

    This is typically used to refer to a related message (such as a reply or forward),
    carrying just enough metadata to identify and order it.
    """

    date: int = Field(..., alias="1")
    """The timestamp of the message in **milliseconds** since epoch."""

    message_id: int = Field(..., alias="2")
    """Unique identifier of the message in the conversation."""

    seq: Optional[int] = Field(None, alias="3")
    """Optional sequence number used for ordering in certain contexts."""

    @model_validator(mode="before")
    @classmethod
    def set_default_message_id(cls, data: Any) -> Any:
        if isinstance(data, dict) and "2" not in data:
            data["2"] = -1
        return data

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            date: int,
            message_id: int,
            seq: Optional[int] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                date=date, message_id=message_id, seq=seq, **__pydantic_kwargs
            )
