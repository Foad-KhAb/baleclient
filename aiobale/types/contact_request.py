from pydantic import Field
from typing import List, Optional, Any

from .base import BaleObject
from .values import StringValue


class ContactData(BaleObject):
    phone_number: int = Field(..., alias="1")
    name: StringValue = Field(..., alias="2")
