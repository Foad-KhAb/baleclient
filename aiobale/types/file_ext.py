from __future__ import annotations

from pydantic import Field, model_validator
from typing import TYPE_CHECKING, Any, Dict, Optional

from .base import BaleObject
from .values import StringValue


class PhotoExt(BaleObject):
    w: Optional[int] = Field(None, alias="1")
    h: Optional[int] = Field(None, alias="2")


class VideoExt(BaleObject):
    w: Optional[int] = Field(None, alias="1")
    h: Optional[int] = Field(None, alias="2")
    duration: Optional[int] = Field(None, alias="3")


class VoiceExt(BaleObject):
    duration: Optional[int] = Field(None, alias="1")


class AudioExt(BaleObject):
    duration: Optional[int] = Field(None, alias="1")
    album: Optional[str] = Field(None, alias="2")
    genre: Optional[str] = Field(None, alias="3")
    track: Optional[str] = Field(None, alias="4")
    
    
class DocumentsExt(BaleObject):
    photo: Optional[PhotoExt] = Field(None, alias="1")
    video: Optional[VideoExt] = Field(None, alias="2")
    voice: Optional[VoiceExt] = Field(None, alias="3")
    audio: Optional[AudioExt] = Field(None, alias="5")
    gif: Optional[VideoExt] = Field(None, alias="4")
