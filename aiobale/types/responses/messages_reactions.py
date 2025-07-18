from __future__ import annotations

from pydantic import Field, ValidationInfo, model_validator
from typing import List, Optional, Any, Dict, TYPE_CHECKING

from ..base import BaleObject
from ..message_reaction import MessageReactions


class ReactionsResponse(BaleObject):
    messages: List[MessageReactions] = Field([], alias="1")
