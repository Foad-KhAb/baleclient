from typing import Any, Dict, Optional
from pydantic import Field, model_validator

from ..enums import PeerSource
from .base import BaleObject
from .peer import Peer


class PeerReport(BaleObject):
    source: PeerSource = Field(..., alias="1")
    peer: Peer = Field(..., alias="2")
