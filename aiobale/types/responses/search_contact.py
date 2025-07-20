from __future__ import annotations

from pydantic import Field
from typing import Optional

from ..base import BaleObject
from ..info_peer import InfoPeer


class ContactResponse(BaleObject):
    user: Optional[InfoPeer] = Field(None, alias="2")
    chat: Optional[InfoPeer] = Field(None, alias="4")
