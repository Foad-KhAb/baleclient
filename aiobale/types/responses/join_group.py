from __future__ import annotations

from typing import Any, Dict, List
from pydantic import Field, model_validator

from ..short_peer import ShortPeer
from ..group import Group
from .default import DefaultResponse


class JoinedGroupResponse(DefaultResponse):
    group: Group = Field(default=None, alias="1")
    random_id: int = Field(..., alias="6")
    users: List[ShortPeer] = Field(default_factory=list, alias="7")
    inviter_id: int = Field(..., alias="8")
    group_seq: int = Field(..., alias="9")

    @model_validator(mode="before")
    @classmethod
    def normalize_lists(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        value = data.get("7")
        if value is not None and not isinstance(value, list):
            data["7"] = [value]
        return data
