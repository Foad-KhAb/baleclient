from io import BytesIO


class Int64VarintCodec:
    """"Codec for encoding and decoding a list of int64 integers using Protobuf varint format."""

    @staticmethod
    def encode_varint(value: int) -> bytes:
        """"Encodes a single int64 integer as a varint (two's complement)."""
        if value < 0:
            value += 1 << 64
        output = bytearray()
        while True:
            byte = value & 0x7F
            value >>= 7
            if value:
                output.append(byte | 0x80)
            else:
                output.append(byte)
                break
        return bytes(output)

    @staticmethod
    def decode_varint(stream: BytesIO) -> int:
        """"Decodes a single varint from the stream and returns it as a signed int64."""
        shift = 0
        result = 0
        while True:
            b = stream.read(1)
            if not b:
                raise EOFError("Unexpected EOF while reading varint")
            byte = b[0]
            result |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7
            if shift >= 70:  # Prevents infinite loop on malformed input
                raise ValueError("Too many bytes when decoding varint")
        if result >= (1 << 63):
            result -= 1 << 64
        return result

    @classmethod
    def encode_list(cls, numbers: list[int]) -> bytes:
        """"Encodes a list of int64 integers into a bytes object using varint encoding."""
        encoded = bytearray()
        for number in numbers:
            encoded.extend(cls.encode_varint(number))
        return bytes(encoded)

    @classmethod
    def decode_list(cls, hex_string: str | bytes) -> list[int]:
        """"Decodes a hex string or bytes containing a sequence of int64 varints into a list of integers."""
        if isinstance(hex_string, str):
            data = bytes.fromhex(hex_string)
        else:
            data = hex_string
        stream = BytesIO(data)
        numbers = []
        while stream.tell() < len(data):
            numbers.append(cls.decode_varint(stream))
        return numbers
