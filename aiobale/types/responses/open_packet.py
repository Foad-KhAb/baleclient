from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING, List
from pydantic import Field, model_validator

from ..base import BaleObject
from ..winner import Winner
from ...enums import GiftOpenning


class PacketResponse(BaleObject):
    receivers: List[Winner] = Field(default_factory=list, alias="1")
    status: GiftOpenning = Field(GiftOpenning.ALREADY_RECEIVED, alias="2")
    openned_count: int = Field(..., alias="3")
    win_amount: int = Field(..., alias="4")
    rank: int = Field(..., alias="5")

    @model_validator(mode="before")
    @classmethod
    def _validate_wallets(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "1" in data and not isinstance(data["1"], list):
            data["1"] = [data["1"]]

        if "4" in data:
            data["4"] = data["4"]["1"]
            
        if "5" in data:
            data["5"] = data["5"]["1"]

        return data
