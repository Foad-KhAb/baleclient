import json
from typing import Any, Dict, Optional
from blackboxprotobuf import decode_message, encode_message
import base64
import traceback


class ProtoBuf:
    def _fix_fields(self, data: bytes) -> Dict[str, Any]:
        if isinstance(data, dict):
            new_data = {}
            for key, value in data.items():
                if "-" in key:
                    key = key.split("-")[0]
                    
                if key == "15" and isinstance(value, dict) and "1" in value:
                    try:
                        raw_bytes = self.encode(value)
                        fixed = self.decode(raw_bytes, {"1": {"type": "str"}})
                        new_data[key] = fixed
                        continue
                    except Exception as e:
                        traceback.print_exception(e)
                        pass
                new_data[key] = self._fix_fields(value)
            return new_data
        elif isinstance(data, list):
            return [self._fix_fields(item) for item in data]
        return data

    def _convert_bytes_to_string(self, obj: bytes) -> Dict[str, Any]:
        if isinstance(obj, dict):
            return {k: self._convert_bytes_to_string(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_bytes_to_string(v) for v in obj]
        elif isinstance(obj, bytes):
            try:
                return obj.decode("utf-8")
            except UnicodeDecodeError:
                return obj.hex()
        else:
            return obj

    def infer_typedef(self, message_dict) -> Dict[str, Any]:
        typedef = {}
        for field_num, value in message_dict.items():
            if isinstance(value, list):
                elem = value[0] if value else {}
                if isinstance(elem, dict):
                    sub_typedef = self.infer_typedef(elem)
                    typedef[field_num] = {
                        "rule": "repeated",
                        "type": "message",
                        "message_typedef": sub_typedef,
                        "name": "",
                    }
                else:
                    base_type = "int" if isinstance(elem, int) else "bytes"
                    typedef[field_num] = {"rule": "repeated", "type": base_type, "name": ""}

            elif isinstance(value, dict):
                sub_typedef = self.infer_typedef(value)
                typedef[field_num] = {
                    "type": "message",
                    "message_typedef": sub_typedef,
                    "name": "",
                }

            elif isinstance(value, int):
                typedef[field_num] = {"type": "int", "name": ""}

            else:
                typedef[field_num] = {"type": "bytes", "name": ""}

        return typedef
    
    def decode(self, value: bytes, type_def: Optional[dict] = None) -> Dict[str, Any]:
        decoded, _ = decode_message(value, type_def)
        return self._convert_bytes_to_string(
            self._fix_fields(decoded)
        )

    def encode(self, data: dict, force_raw: bool = True) -> bytes:
        typedef = self.infer_typedef(data)
        encoded = encode_message(data, typedef)

        if force_raw:
            return encoded
        return base64.b64encode(encoded).decode("utf-8")
