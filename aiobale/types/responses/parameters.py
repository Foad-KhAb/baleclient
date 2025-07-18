from pydantic import Field
from typing import List

from ..base import BaleObject
from ..ext import ExtKeyValue


class ParametersResponse(BaleObject):
    params: List[ExtKeyValue] = Field([], alias="1")
