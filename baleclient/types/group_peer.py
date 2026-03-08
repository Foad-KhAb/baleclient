from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from .base import BaleObject


class GroupPeer(BaleObject):
    """
    Represents a minimal reference to a group or channel peer.

    This object usually appears in responses where only the peer identifier
    and its access hash are returned.
    """

    id: int = Field(..., alias="1")
    """Unique identifier of the group or channel."""

    access_hash: int = Field(..., alias="2")
    """
    Access hash associated with the peer.

    This value is typically required for performing further API calls
    involving the same group or channel.
    """

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            id: int,
            access_hash: int,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(id=id, access_hash=access_hash, **__pydantic_kwargs)
