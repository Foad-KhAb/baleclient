from typing import Any, Dict
from pydantic import Field, model_validator

from .base import BaleObject


class BanData(BaleObject):
    banned_id: int = Field(..., alias="1")
    banner_id: int = Field(..., alias="2")
    
    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str , Any]:
        for key in list(data.keys()):
            value = data[key]

            if isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]

        return data
