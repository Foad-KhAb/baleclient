from pydantic import Field
from typing import TYPE_CHECKING, Any, List

from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class ResetContacts(BaleMethod):
    __service__ = Services.USER.value
    __method__ = "ResetContacts"
    
    __returning__ = DefaultResponse
