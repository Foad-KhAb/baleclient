from pydantic import Field
from typing import Optional

from ..int_bool import IntBool
from ..base import BaleObject
from ...enums import SendCodeType


class Value(BaleObject):
    value: int = Field(..., alias="1")


class PhoneAuthResponse(BaleObject):
    transaction_hash: str = Field(..., alias="1")
    is_registered: IntBool = Field(..., alias="2")
    sent_code_type: SendCodeType = Field(..., alias="5")
    code_expiration_date: Value = Field(..., alias="6")
    next_send_code_type: Optional[SendCodeType] = Field(None, alias="7")
    code_timeout: Value = Field(..., alias="8")
