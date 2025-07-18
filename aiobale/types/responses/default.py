from pydantic import Field
from typing import Optional, List

from ..base import BaleObject


class DefaultResponse(BaleObject):
    seq: Optional[int] = Field(None, alias="1")
    data: Optional[int] = Field(None, alias="2")
