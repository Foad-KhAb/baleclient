from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING, Union

from .base import BaleObject


class Thumbnail(BaleObject):
    w: int = Field(..., alias="1")
    h: int = Field(..., alias="2")
    image: Union[str, bytes] = Field(..., alias="3")
