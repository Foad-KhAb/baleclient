from pydantic import Field
from typing import List, Optional, Any

from .ext import ExtData
from .base import BaleObject
from .auth import AuthBody
    
    
class MetaList(BaleObject):
    meta_list: List[ExtData] = Field(..., alias="1")


class RequestBody(BaleObject):
    service: str = Field(..., alias="1")
    method: str = Field(..., alias="2")
    payload: Optional[Any] = Field(None, alias="3")
    metadata: MetaList = Field(..., alias="4")
    request_id: int = Field(..., alias="5")


class Request(BaleObject):
    body: Optional[RequestBody] = Field(None, alias="1")
    auth: Optional[AuthBody] = Field(None, alias="3")
