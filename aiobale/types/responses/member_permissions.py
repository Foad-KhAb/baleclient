from __future__ import annotations

from pydantic import Field

from ..base import BaleObject
from ..permissions import Permissions


class MemberPermissionsResponse(BaleObject):
    permissions: Permissions = Field(..., alias="1")
