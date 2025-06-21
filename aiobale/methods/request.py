from pydantic import Field
from typing import List, Any, Optional

from .base import BaleMethod


class MetaValue(BaleMethod):
    name: str = Field(..., alias="1")


class MetaData(BaleMethod):
    name: str = Field(..., alias="1")
    values: MetaValue = Field(..., alias="2")
    

class MetaList(BaleMethod):
    meta_list: List[MetaData] = Field(..., alias="1")


class RequestBody(BaleMethod):
    service: str = Field(..., alias="1")
    method: str = Field(..., alias="2")
    payload: Optional[Any] = Field(None, alias="3")
    metadata: MetaList = Field(..., alias="4")
    number: int = Field(..., alias="5")
    

class Request(BaleMethod):
    body: RequestBody = Field(..., alias="1")
