from pydantic import Field
from typing import TYPE_CHECKING, Any, List

from ...types.responses import UsersResponse
from ...enums import Services
from ..base import BaleMethod


class LoadBlockedUsers(BaleMethod):
    __service__ = Services.USER.value
    __method__ = "LoadBlockedUsers"
    
    __returning__ = UsersResponse
