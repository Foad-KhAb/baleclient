import json
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from pydantic import Field, model_validator

from ..base import BaleObject


class UpvotersResponse(BaleObject):
    count: Optional[int] = None
    offset: Optional[int] = None
    users: List[int] = Field(default_factory=list)

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            limit: int,
            offset: int,
            users: List[int],
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                limit=limit, offset=offset, users=users, **__pydantic_kwargs
            )
            
    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "1" in data:
            offset_info = json.loads(data["1"]["1"])
            data.update(offset_info)
            
        if "2" in data:
            data["users"] = [user["1"] for user in data["2"]]
        
        return data
