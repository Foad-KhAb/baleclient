from typing import Any, Dict, List, Optional
from pydantic import Field, model_validator

from ..enums import ChatType, PrivacyMode
from .int_bool import IntBool
from .base import BaleObject


class ExInfo(BaleObject):
    expeer_type: ChatType = Field(..., alias="1")
    identified: IntBool = Field(False, alias="2")


class FullUser(BaleObject):
    id: int = Field(..., alias="1")
    about: Optional[str] = Field(None, alias="3")
    languages: Optional[List[str]] = Field(None, alias="4")
    timezone: Optional[str] = Field(None, alias="5")
    is_blocked: IntBool = Field(False, alias="6")
    ex_info: ExInfo = Field(..., alias="9")
    is_deleted: IntBool = Field(False, alias="12")
    is_contact: IntBool = Field(False, alias="13")
    created_at: int = Field(..., alias="15")
    privacy_mode: PrivacyMode = Field(..., alias="16")
    allowed_invite: IntBool = Field(False, alias="17")
    
    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str , Any]:
        for key in list(data.keys()):
            value = data[key]

            if isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]

            elif not value:
                data.pop(key)

            elif key == "4" and not isinstance(data[key], list):
                data[key] = [data[key]]

        return data
