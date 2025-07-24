from pydantic import Field
from typing import TYPE_CHECKING, Optional

from ...types import Chat, SendTypeModel, FileUploadInfo
from ...enums import Services
from ..base import BaleMethod


class GetFileUploadUrl(BaleMethod):
    __service__ = Services.FILES.value
    __method__ = "GetNasimFileUploadUrl"

    __returning__ = FileUploadInfo

    expected_size: int = Field(..., alias="1")
    user_id: int = Field(..., alias="3")
    name: str = Field(..., alias="4")
    mime_type: str = Field(..., alias="5")
    chat: Optional[Chat] = Field(None, alias="6")
    send_type: Optional[SendTypeModel] = Field(None, alias="7")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            expected_size: int,
            user_id: int,
            name: int,
            mime_type: int,
            chat: Chat,
            send_type: Optional[SendTypeModel],
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                expected_size=expected_size,
                user_id=user_id,
                name=name,
                mime_type=mime_type,
                chat=chat,
                send_type=send_type,
                **__pydantic_kwargs
            )
