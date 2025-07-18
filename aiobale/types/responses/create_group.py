from __future__ import annotations

from typing import Any, Dict, List
from pydantic import Field, model_validator

from ..short_peer import ShortPeer
from ..group import Group
from .default import DefaultResponse


class GroupCreatedResponse(DefaultResponse):
    group: Group = Field(default=None, alias="3")
    users: List[ShortPeer] = Field(default_factory=list, alias="5")
    not_added_users: List[ShortPeer] = Field(default_factory=list, alias="6")
    invite_link: str = Field(..., alias="7")

    @model_validator(mode="before")
    @classmethod
    def normalize_lists(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure fields '5' and '6' are always lists."""
        for key in ("5", "6"):
            value = data.get(key)
            if value is not None and not isinstance(value, list):
                data[key] = [value]
        return data
