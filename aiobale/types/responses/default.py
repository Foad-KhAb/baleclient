from pydantic import Field
from typing import Optional, Any, List

from ..ext import ExtData
from ..base import BaleObject


class DefaultResponse(BaleObject):
    seq: int = Field(..., alias="1")
    data: int = Field(..., alias="2")
    ext: List[ExtData] = Field(..., alias="4")
