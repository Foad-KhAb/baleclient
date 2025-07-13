from typing import Optional
from pydantic import Field

from ..enums import PeerType
from .base import BaleObject


class InfoPeer(BaleObject):
    id: int = Field(..., alias="1")
    type: PeerType = Field(..., alias="2")
