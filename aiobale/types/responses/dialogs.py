from __future__ import annotations

from pydantic import Field, model_validator
from typing import Any, Dict, List

from ..peer_data import PeerData
from ..base import BaleObject


class DialogResponse(BaleObject):
    dialogs: List[PeerData] = Field(..., alias="3")
