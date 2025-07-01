from __future__ import annotations

from typing import Final, Callable, Any, Optional, Type
from types import TracebackType
import abc

from ...utils import ProtoBuf
from ...methods import BaleMethod, BaleType


_Decoder = Callable[..., Any]
_Encoder = Callable[..., dict]

BALE_WS: Final[str] = "wss://next-ws.bale.ai/ws/"
DEFAULT_TIMEOUT: Final[float] = 5.0


class BaseSession(abc.ABC):
    def __init__(
        self,
        ws_url: str = BALE_WS,
        decoder: _Decoder = ProtoBuf().decode,
        encoder: _Encoder = ProtoBuf().encode,
        timeout: float = DEFAULT_TIMEOUT
    ) -> None:

        self.ws_url = ws_url
        self.decoder = decoder
        self.encoder = encoder
        self.timeout = timeout
        self._request_number = 0
        
    @abc.abstractmethod
    async def close(self) -> None:
        pass
        
    @abc.abstractmethod
    async def make_request(
        self,
        method: BaleMethod[BaleType],
        timeout: Optional[int] = None
    ) -> BaleType:
        pass
    
    def next_request_number(self) -> int:
        self._request_number += 1
        return self._request_number
    
    async def __aenter__(self) -> BaseSession:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.close()
