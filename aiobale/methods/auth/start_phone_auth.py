from pydantic import Field
from typing import TYPE_CHECKING, Any, Optional

from ...types.responses import PhoneAuthResponse
from ...enums import Services, SendCodeType
from ..base import BaleMethod


class StartPhoneAuth(BaleMethod):
    __service__ = Services.AUTH.value
    __method__ = "StartPhoneAuth"
    
    __returning__ = PhoneAuthResponse

    phone_number: int = Field(..., alias="1")
    app_id: int = Field(..., alias="2")
    app_key: str = Field(..., alias="3")
    device_hash: str = Field(..., alias="4")
    device_title: str = Field(..., alias="5")
    send_code_type: SendCodeType = Field(..., alias="9")
    options: Optional[dict] = Field(default_factory=lambda: {"0": 1}, alias="10")

    # This __init__ is only for type hinting and IDE autocomplete.
    if TYPE_CHECKING:
        def __init__(
            self,
            *,
            phone_number: int,
            app_id: int,
            app_key: str,
            device_hash: str,
            device_title: str,
            send_code_type: SendCodeType = SendCodeType.DEFAULT,
            options: Optional[dict] = None,
            **kwargs: Any,
        ) -> None:
            super().__init__(
                phone_number=phone_number,
                app_id=app_id,
                app_key=app_key,
                device_hash=device_hash,
                device_title=device_title,
                send_code_type=send_code_type,
                options=options,
                **kwargs,
            )
