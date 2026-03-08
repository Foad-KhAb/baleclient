from __future__ import annotations

from typing import TYPE_CHECKING, List

from pydantic import Field

from .base import BaleObject
from .other_message import OtherMessage
from .peer import Peer


class MessageReport(BaleObject):
    """
    Represents a report of messages related to a specific peer in the Bale messaging platform.
    """

    peer: Peer = Field(..., alias="1")
    """The target peer (user, chat, or channel) that the report is about."""

    messages: List[OtherMessage] = Field(..., alias="2")
    """A list of messages related to the peer, typically used for reporting or analysis."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            messages: List[OtherMessage],
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(peer=peer, messages=messages, **__pydantic_kwargs)
