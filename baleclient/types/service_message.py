from pydantic import Field

from .base import BaleObject
from .service_ext import ServiceExt


class ServiceMessage(BaleObject):
    text: str = Field(..., alias="1")
    ext: ServiceExt = Field(..., alias="2")
