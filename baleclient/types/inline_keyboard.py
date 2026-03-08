from typing import TYPE_CHECKING, Any, List, Optional

from pydantic import Field, model_serializer, model_validator

from .base import BaleObject


class InlineKeyboardButton(BaleObject):
    """
    Represents a button within an inline keyboard.
    """

    text: str = Field(..., alias="1")
    """Label text displayed on the button."""

    url: Optional[str] = Field(None, alias="2")
    """URL to be opened when the button is pressed."""

    callback_data: Optional[str] = Field(None, alias="3")
    """Data sent back to the bot when the button is pressed."""

    copy_text: Optional[str] = Field(None, alias="9")
    """Text to be copied to the clipboard when the button is pressed."""

    if TYPE_CHECKING:
        # This __init__ is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            text: str,
            url: Optional[str] = None,
            callback_data: Optional[str] = None,
            copy_text: Optional[str] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                text=text,
                url=url,
                callback_data=callback_data,
                copy_text=copy_text,
                **__pydantic_kwargs,
            )

    @model_validator(mode="before")
    @classmethod
    def validate_keyboard(cls, data):
        """
        Extracts nested field values from the serialized form
        into the expected flat model structure before validation.
        API nested fields:
          "2": {"1": "..."}  OR  "2": {}  OR missing
        Convert to:
          "2": "..." OR None
        """
        if not isinstance(data, dict):
            return data

        for key in ("2", "3", "9"):
            if key not in data:
                continue

            v = data[key]

            # Empty dict -> treat as None
            if isinstance(v, dict) and not v:
                data[key] = None
                continue

            # {"1": "..."} -> unwrap
            if isinstance(v, dict) and "1" in v:
                data[key] = v["1"]
                continue

            # already a string (or something) -> leave as is
        return data

    @model_serializer(mode="wrap")
    def ser(self, nxt, info):
        """
        Serialize to API nested alias structure:
          "2": {"1": "..."}
        """
        if not info.by_alias:
            return nxt(self)

        out = nxt(self)
        for key in ("2", "3", "9"):
            if key not in out:
                continue
            if out[key] is None:
                out.pop(key, None)
                continue
            out[key] = {"1": out[key]}
        return out


class InlineKeyboardMarkup(BaleObject):
    """
    Represents the entire inline keyboard layout for a message.
    """

    inline_keyboard: List[List[InlineKeyboardButton]] = Field(
        default_factory=list, alias="1"
    )
    """Two-dimensional array of inline keyboard button rows."""

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

    @staticmethod
    def _unwrap_1(v: Any) -> Any:
        # unwrap nested {"1": {"1": {"1": ...}}}
        while isinstance(v, dict) and set(v.keys()) == {"1"}:
            v = v["1"]
        return v

    @model_validator(mode="before")
    @classmethod
    def validate_keyboard(cls, data: Any):
        if not isinstance(data, dict) or "1" not in data:
            return data

        raw = cls._unwrap_1(data["1"])

        keyboard_rows: List[List[InlineKeyboardButton]] = []

        # Case A) raw is a single button dict -> make it [[button]]
        if isinstance(raw, dict):
            raw_btn = cls._unwrap_1(raw)
            btn = InlineKeyboardButton.model_validate(raw_btn)
            keyboard_rows.append([btn])
            return {"1": keyboard_rows}

        # Case B) raw is rows list
        if isinstance(raw, list):
            for row in raw:
                row_unwrapped = cls._unwrap_1(row)

                # row could be dict (single button) or list (multiple buttons)
                if isinstance(row_unwrapped, dict):
                    btn = InlineKeyboardButton.model_validate(
                        cls._unwrap_1(row_unwrapped)
                    )
                    keyboard_rows.append([btn])
                elif isinstance(row_unwrapped, list):
                    btns: List[InlineKeyboardButton] = []
                    for b in row_unwrapped:
                        b_unwrapped = cls._unwrap_1(b)
                        if isinstance(b_unwrapped, dict):
                            btns.append(
                                InlineKeyboardButton.model_validate(b_unwrapped)
                            )
                    keyboard_rows.append(btns)

            return {"1": keyboard_rows}

        # unknown shape, leave it
        return data
