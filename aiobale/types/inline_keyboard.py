from typing import List, Optional, TYPE_CHECKING
from pydantic import Field, model_serializer, model_validator

from .base import BaleObject


class InlineKeyboardButton(BaleObject):
    text: str = Field(..., alias="1")
    url: Optional[str] = Field(None, alias="2")
    callback_data: Optional[str] = Field(None, alias="3")
    copy_text: Optional[str] = Field(None, alias="9")

    @model_validator(mode="before")
    @classmethod
    def validate_keyboard(cls, data):
        if isinstance(data, dict) and "1" in data:
            for i in ("2", "3", "9"):
                if i not in data:
                    continue
                data[i] = data[i]["1"]
        return data

    @model_serializer(mode="wrap")
    def ser(self, nxt, info):
        if not info.by_alias:
            return nxt(self)

        out = nxt(self)
        for i in ("2", "3", "9"):
            if i not in out:
                continue
            out[i] = {"1": out[i]}
        return out


class InlineKeyboardMarkup(BaleObject):
    inline_keyboard: List[List[InlineKeyboardButton]] = Field(
        default_factory=list, alias="1"
    )

    if TYPE_CHECKING:
        # This __init__ is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            inline_keyboard: List[List[InlineKeyboardButton]],
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(inline_keyboard=inline_keyboard, **__pydantic_kwargs)

    @model_validator(mode="before")
    @classmethod
    def validate_keyboard(cls, data):
        if isinstance(data, dict) and "1" in data and isinstance(data["1"], list):
            raw_buttons = data["1"]

            keyboard_rows = []
            for row in raw_buttons:
                if isinstance(row, dict) and "1" in row:
                    buttons_dict = row["1"]
                    btn = InlineKeyboardButton.model_validate(buttons_dict)
                    keyboard_rows.append([btn])
                else:
                    pass

            return {"1": keyboard_rows}
        return data

    @model_serializer(mode="wrap")
    def ser(self, nxt, info):
        if not info.by_alias:
            return nxt(self)

        out = []
        for row in self.inline_keyboard:
            buttons_serialized = [
                btn.model_dump(by_alias=True, exclude_none=True) for btn in row
            ]
            out.append({"1": buttons_serialized})
        return {"1": out}
