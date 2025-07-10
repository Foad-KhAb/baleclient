from pydantic import Field
from typing import Optional, List

from ..ext import ExtData
from ..base import BaleObject


class DefaultResponse(BaleObject):
    seq: int = Field(..., alias="1")
    data: Optional[int] = Field(None, alias="2")
    ext: Optional[List[ExtData]] = Field(None, alias="4")
