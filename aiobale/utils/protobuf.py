from blackboxprotobuf import decode_message, encode_message
import base64


class ProtoBuf:
    def _convert_bytes_to_string(self, obj):
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

    def infer_typedef(self, message_dict):
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
    
    def decode(self, value: str | bytes, b64: bool = False):
        if b64:
            value = base64.b64decode(value)

        decoded, _ = decode_message(value)
        return self._convert_bytes_to_string(decoded)

    def encode(self, data: dict, force_raw: bool = True):
        typedef = self.infer_typedef(data)
        encoded = encode_message(data, typedef)

        if force_raw:
            return encoded
        return base64.b64encode(encoded).decode("utf-8")
