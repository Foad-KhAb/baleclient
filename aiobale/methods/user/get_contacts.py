from pydantic import Field
from typing import TYPE_CHECKING, Any, List

from ...types.responses import BlockedUsersResponse
from ...enums import Services
from ..base import BaleMethod


class GetContacts(BaleMethod):
    __service__ = Services.USER.value
    __method__ = "GetContacts"
    
    __returning__ = BlockedUsersResponse
