from __future__ import annotations

from pydantic import Field, model_validator
from typing import Any, Dict, List

from ..base import BaleObject
from ..file_url import FileURL


class FileURLResponse(BaleObject):
    file_urls: List[FileURL] = Field(default_factory=list, alias="1")
    
    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "1" not in data:
            return data
        
        if not isinstance(data["1"], list):
            data["1"] = [data["1"]]
        
        return data
