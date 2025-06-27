from pydantic import Field
from typing import List, Optional, Any

from .ext import ExtData
from .base import BaleObject
    
    
class MetaList(BaleObject):
    meta_list: List[ExtData] = Field(..., alias="1")


class RequestBody(BaleObject):
    service: str = Field(..., alias="1")
    method: str = Field(..., alias="2")
    payload: Optional[Any] = Field(None, alias="3")
    metadata: MetaList = Field(..., alias="4")
    number: int = Field(..., alias="5")


class Request(BaleObject):
    body: RequestBody = Field(..., alias="1")
