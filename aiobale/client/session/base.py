import abc
from typing import Final, Callable, Any, Optional

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

        self.ws_url = ws_url,
        self.decoder = decoder
        self.encoder = encoder
        self.timeout = timeout
        
    @abc.abstractmethod
    async def make_request(
        self,
        method: BaleMethod[BaleType],
        timeout: Optional[int] = None
    ) -> BaleType:
        pass
