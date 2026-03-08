import base64
import json
import re
from typing import Any, Optional

JWT_RE = re.compile(
    rb"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"
)


def clean_grpc(data: bytes) -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(f"Expected bytes, got {type(data)}")

    if len(data) < 5:
        return data

    compressed = data[0]
    msg_len = int.from_bytes(data[1:5], "big")

    if compressed not in (0, 1):
        raise ValueError(f"Invalid gRPC compression flag: {compressed}")

    end = 5 + msg_len
    if len(data) < end:
        raise ValueError(
            f"Incomplete gRPC payload: expected {msg_len}, got {len(data) - 5}"
        )

    return data[5:end]


def extract_jwt_from_bytes(data: bytes) -> Optional[str]:
    m = JWT_RE.search(data)
    return m.group(0).decode("ascii") if m else None


def decode_jwt_payload(token: str) -> dict[str, Any]:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return {}

        payload_b64 = parts[1]
        padding = "=" * (-len(payload_b64) % 4)
        raw = base64.urlsafe_b64decode(payload_b64 + padding)
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return {}


def maybe_extract_name_from_bytes(data: bytes) -> Optional[str]:
    """
    Best-effort name extraction from corrupted payload.
    """
    try:
        text = data.decode("utf-8", errors="ignore")
    except Exception:
        return None

    candidates = re.findall(r"[\u0600-\u06FFA-Za-z0-9 _-]{3,40}", text)
    for c in candidates:
        c = c.strip()
        if not c:
            continue
        if "eyJhbGciOi" in c or "grpc-status" in c:
            continue
        return c
    return None


def add_header(payload: bytes):
    compressed_flag = 0x00
    length = len(payload)
    header = bytes([compressed_flag]) + length.to_bytes(4, byteorder="big")

    return header + payload
