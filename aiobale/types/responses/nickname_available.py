from pydantic import Field
from typing import Optional

from ..base import BaleObject
from ..int_bool import IntBool
from .default import DefaultResponse


class NickNameAvailable(DefaultResponse):
    availbale: IntBool = Field(False, alias="1")
