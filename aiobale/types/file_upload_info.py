from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING

from .base import BaleObject


class FileUploadInfo(BaleObject):
    file_id: int = Field(..., alias="1")
    """Unique identifier for the file."""
    url: str = Field(..., alias="2")
    chunk_size: int = Field(262144, alias="4")
