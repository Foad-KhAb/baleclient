from pydantic import Field, model_validator
from typing import Any, Dict, List

from .base import BaleObject
from .peer import Peer
from ..utils import Int64VarintCodec


class SelectedMessages(BaleObject):
    peer: Peer = Field(..., alias="1")
    ids: List[int] = Field(..., alias="2")
    dates: List[int] = Field(..., alias="3")
    
    @model_validator(mode="before")
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["2"] = Int64VarintCodec().decode_list(data["2"])
        data["3"] = Int64VarintCodec().decode_list(data["3"]["1"])
        
        return data
