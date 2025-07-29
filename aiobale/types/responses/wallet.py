from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING, Optional
from pydantic import Field, model_validator

from ..base import BaleObject
from ..wallet import Wallet


class WalletResponse(BaleObject):
    wallet: Optional[Wallet] = Field(None, alias="1")
    first_name: Optional[str] = Field(None, alias="2")
    last_name: Optional[str] = Field(None, alias="3")

    @model_validator(mode="before")
    @classmethod
    def _validate_wallets(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "1" in data and isinstance(data["1"], list):
            data["1"] = data["1"][0] if data["1"] else None
            
        for key in list(data.keys()):
            value = data[key]
            if isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]
        return data
