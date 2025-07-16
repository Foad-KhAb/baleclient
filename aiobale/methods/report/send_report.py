from pydantic import Field
from typing import TYPE_CHECKING

from ...types import Report
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class SendReport(BaleMethod):
    __service__ = Services.REPORT.value
    __method__ = "ReportInappropriateContent"
    
    __returning__ = DefaultResponse
    
    report_body: Report = Field(..., alias="1")
    
    if TYPE_CHECKING:
        # Just For Type Helping
        
        def __init__(
            __pydantic__self__,
            *,
            report_body: Report,
            **__pydantic_kwargs
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            
            super().__init__(
                report_body=report_body,
                **__pydantic_kwargs
            )
