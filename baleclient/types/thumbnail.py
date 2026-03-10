from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union

from pydantic import Field, model_validator

from .base import BaleObject


class Thumbnail(BaleObject):
    """
    Represents a thumbnail image with size and image data.

    This is typically used to provide a small preview version of a media file.
    The image data can either be:
    - A URL (if the image is hosted remotely)
    - Raw bytes (if embedded directly in the structure)
    """

    w: int = Field(..., alias="1")
    """Width of the thumbnail in pixels."""

    h: int = Field(..., alias="2")
    """Height of the thumbnail in pixels."""

    image: Union[str, bytes] = Field(..., alias="3")
    """Thumbnail image data. Can be either:

    - `str`: a URL pointing to the image
    - `bytes`: raw image bytes (e.g., in base64 or binary format)
    """
    raw_meta: Optional[dict] = Field(None, exclude=True)

    @model_validator(mode="before")
    @classmethod
    def normalize_thumb(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        image_value = data.get("3")

        # Case 1: image is wrapped in a dict with metadata
        if isinstance(image_value, dict):
            data["raw_meta"] = image_value

            # Prefer the embedded bytes if present
            if isinstance(image_value.get("10"), (bytes, bytearray)):
                data["3"] = bytes(image_value["10"])
            # Fallback: stringify or fail more gracefully
            elif isinstance(image_value.get("10"), str):
                data["3"] = image_value["10"]
            else:
                data["3"] = b""

        return data

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            w: int,
            h: int,
            image: Union[str, bytes],
            raw_meta: Optional[dict] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                w=w,
                h=h,
                image=image,
                raw_meta=raw_meta,
                **__pydantic_kwargs,
            )
