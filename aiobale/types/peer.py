from pydantic import Field

from ..enums import PeerType
from .base import BaleObject


class Peer(BaleObject):
    type: PeerType = Field(..., alias="1")
    id: int = Field(..., alias="2")
