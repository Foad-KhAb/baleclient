from __future__ import annotations

from typing import Final, Callable, Any, Optional, List, TYPE_CHECKING
import abc
import time

from ...utils import ProtoBuf
from ...methods import BaleMethod, BaleType
from ...types import Request, RequestBody, AuthBody, ExtData, ExtValue, MetaList

if TYPE_CHECKING:
    from ..client import Client


_Decoder = Callable[..., dict]
_Encoder = Callable[..., bytes]

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
        self._request_id = 0
        self.session_id = int(time.time() * 1000)
        
    def build_payload(self, method: BaleMethod[BaleType], request_id: int) -> bytes:
        request = Request(
            body=RequestBody(
                service=method.__service__,
                method=method.__method__,
                payload=method,
                metadata=self._get_meta_data(),
                request_id=request_id
            )
        )
        
        payload = request.model_dump(by_alias=True, exclude_none=True)
        return self.encoder(payload)
    
    def decode_result(self, result: Any, method: BaleMethod[BaleType], client: Client) -> Any:
        result["client_cls"] = client
        result["method_data"] = method
        
        model_type = method.__returning__
        return model_type.model_validate(result)
    
    def get_login_payload(self) -> bytes:
        request = Request(
            auth=AuthBody(
                authorized=1,
                ready=1
            )
        )
        
        payload = request.model_dump(by_alias=True, exclude_none=True)
        return self.encoder(payload)
    
    def _get_meta_data(self) -> MetaList:
        data = {
            'app_version': "105249",
            'browser_type': "1",
            'browser_version': "135.0.0.0",
            'os_type': "3",
            'session_id': str(self.session_id),
            'mt_app_version': "105249",
            'mt_browser_type': "1",
            'mt_browser_version': "135.0.0.0",
            'mt_os_type': "3",
            'mt_session_id': str(self.session_id)
        }
        
        ext = []
        for key, value in data.items():
            ext.append(
                ExtData(
                    name=key,
                    value=ExtValue(
                        string=value
                    )
                )
            )
            
        return MetaList(meta_list=ext)
        
    @abc.abstractmethod
    async def close(self) -> None:
        pass
    
    @abc.abstractmethod
    async def connect(self, token: str) -> None:
        pass
    
    @abc.abstractmethod
    async def login_request(self) -> None:
        pass
        
    @abc.abstractmethod
    async def make_request(
        self,
        method: BaleMethod[BaleType],
        timeout: Optional[int] = None
    ) -> BaleType:
        pass
    
    def _next_request_id(self) -> int:
        self._request_id += 1
        return self._request_id
