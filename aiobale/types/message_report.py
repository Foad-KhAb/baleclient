from __future__ import annotations

from pydantic import Field
from typing import List

from .base import BaleObject
from .peer import Peer
from .other_message import OtherMessage


class MessageReport(BaleObject):
    peer: Peer = Field(..., alias="1")
    messages: List[OtherMessage] = Field(..., alias="2")
