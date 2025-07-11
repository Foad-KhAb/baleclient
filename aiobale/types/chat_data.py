from pydantic import Field, model_validator
from typing import Any, Dict, List

from .base import BaleObject
from .peer import Peer
from ..utils import Int64VarintCodec


class PeerData(BaleObject):
    peer: Peer = Field(..., alias="1")
