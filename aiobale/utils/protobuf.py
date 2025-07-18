from typing import Any, Dict, Optional
from blackboxprotobuf import decode_message, encode_message
import base64
import unicodedata
import re


def _is_valid_text(s: str) -> bool:
    if not isinstance(s, str) or len(s.strip()) < 2:
        return False

    escape_like = len(re.findall(r'(\\x[0-9a-fA-F]{2}|\\n|\\r|\\t)', s))
    if escape_like / max(len(s), 1) > 0.1:
        return False

    printable_chars = 0
    total_chars = 0
    for c in s:
        if c.isspace():
            continue
        cat = unicodedata.category(c)
        if cat.startswith(('L', 'N', 'P')):
            printable_chars += 1
        total_chars += 1

    if total_chars == 0:
        return False

    return (printable_chars / total_chars) > 0.8


class ProtoBuf:
    def _fix_fields(self, data: bytes) -> Dict[str, Any]:
        if isinstance(data, dict):
            new_data = {}
            for key, value in data.items():
                if "-" in key:
                    key = key.split("-")[0]

                fixed_value = None
                if isinstance(value, dict):
                    try:
                        raw_bytes = self.encode(value)
                        decoded = self.decode(raw_bytes, {"1": {"type": "str"}})
                        text = decoded.get("1")
                        if _is_valid_text(text):
                            fixed_value = {"1": text}
                    except:
                        pass

                new_data[key] = fixed_value if fixed_value is not None else self._fix_fields(value)
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
