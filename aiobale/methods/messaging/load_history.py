from pydantic import Field
from typing import TYPE_CHECKING, Any, Optional

from ...types import Peer
from ...types.responses import HistoryResponse
from ...enums import Services, ListLoadMode
from ..base import BaleMethod


class LoadHistory(BaleMethod):
    __service__ = Services.MESSAGING.value
    __method__ = "LoadHistory"

    __returning__ = HistoryResponse

    peer: Peer = Field(..., alias="1")
    offset_date: int = Field(..., alias="2")
    load_mode: ListLoadMode = Field(..., alias="4")
    limit: int = Field(..., alias="5")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peer: Peer,
            offset_date: int,
            load_mode: ListLoadMode,
            limit: int,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                peer=peer,
                offset_date=offset_date,
                load_mode=load_mode,
                limit=limit,
                **__pydantic_kwargs
            )
