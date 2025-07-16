from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING, Optional

from ..enums import ReportKind
from .base import BaleObject
from .message_report import MessageReport
from .peer_report import PeerReport


class Report(BaleObject):
    kind: ReportKind = Field(..., alias="1")
    description: Optional[str] = Field(None, alias="2")
    peer_report: Optional[PeerReport] = Field(None, alias="101")
    message_report: Optional[MessageReport] = Field(None, alias="102")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            kind: ReportKind,
            description: Optional[str] = None,
            peer_report: Optional[PeerReport] = None,
            message_report: Optional[MessageReport] = None,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                kind=kind,
                description=description,
                peer_report=peer_report,
                message_report=message_report,
                **__pydantic_kwargs
            )
