from typing import Any, Dict, List, Optional
from pydantic import Field, model_validator

from .base import BaleObject
from .int_bool import IntBool


class Permissions(BaleObject):
    see_message: IntBool = Field(False, alias="1")
    delete_message: IntBool = Field(False, alias="2")
    kick_user: IntBool = Field(False, alias="3")
    pin_message: IntBool = Field(False, alias="4")
    invite_user: IntBool = Field(False, alias="5")
    add_admin: IntBool = Field(False, alias="6")
    change_info: IntBool = Field(False, alias="7")
    send_message: IntBool = Field(False, alias="8")
    see_members: IntBool = Field(False, alias="9")
    edit_message: IntBool = Field(False, alias="10")
    send_media: IntBool = Field(False, alias="11")
    send_gif_stickers: IntBool = Field(False, alias="12")
    reply_to_story: IntBool = Field(False, alias="13")
    forward_message_from: IntBool = Field(False, alias="14")
    send_gift_packet: IntBool = Field(False, alias="15")
    start_call: IntBool = Field(False, alias="16")
    send_link_message: IntBool = Field(False, alias="17")
    send_forwarded_message: IntBool = Field(False, alias="18")
    add_story: IntBool = Field(False, alias="19")
    manage_call: IntBool = Field(False, alias="20")
    
    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str , Any]:
        for key in list(data.keys()):
            value = data[key]
            
            if isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]

            elif not value:
                data.pop(key)
                
        return data
    
    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        for key, value in data.copy().items():
            try:
                int_key = int(key)
            except ValueError:
                continue
            
            if 10 < int_key:
                data[key] = {"1": value}
            
        return data
