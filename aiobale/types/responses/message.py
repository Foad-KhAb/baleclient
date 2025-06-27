from typing import Optional

from ..message import Message
from .default import DefaultResponse


class MessagetResponse(DefaultResponse):
    message: Optional[Message]
