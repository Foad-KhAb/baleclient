from pydantic import Field
from typing import List, Any, Optional

from .base import BaleObject


class MetaValue(BaleObject):
    name: str = Field(..., alias="1")


class MetaData(BaleObject):
    name: str = Field(..., alias="1")
    values: MetaValue = Field(..., alias="2")
    

class MetaList(BaleObject):
    meta_list: List[MetaData] = Field(..., alias="1")


class RequestBody(BaleObject):
    service: str = Field(..., alias="1")
    method: str = Field(..., alias="2")
    payload: Optional[Any] = Field(..., alias="3")
    metadata: MetaList = Field(..., alias="4")
    number: int = Field(..., alias="5")
    

class Request(BaleObject):
    body: RequestBody = Field(..., alias="1")
