from __future__ import annotations

from typing import Final, Callable, Any, Optional, List, TYPE_CHECKING
import abc
import time

from ...utils import ProtoBuf
from ...methods import BaleMethod, BaleType
from ...types import (
    Request, 
    RequestBody, 
    AuthBody, 
    ExtData, 
    ExtValue, 
    MetaList,
    UpdateBody
)

if TYPE_CHECKING:
    from ..client import Client


_Decoder = Callable[..., dict]
_Encoder = Callable[..., bytes]

BALE_WS: Final[str] = "wss://next-ws.bale.ai/ws/"
BALE_URL: Final[str] = "https://next-ws.bale.ai"
DEFAULT_TIMEOUT: Final[float] = 5.0


class BaseSession(abc.ABC):
    def __init__(
        self,
        ws_url: str = BALE_WS,
        post_url: str = BALE_URL,
        decoder: _Decoder = ProtoBuf().decode,
        encoder: _Encoder = ProtoBuf().encode,
        timeout: float = DEFAULT_TIMEOUT
    ) -> None:
        self.ws_url = ws_url
        self.post_url = post_url
        self.decoder = decoder
        self.encoder = encoder
        self.timeout = timeout
        self._request_id = 0
        self.session_id = int(time.time() * 1000)
        
        self.client: Optional[Client] = None
        
    def _bind_client(self, client: Client) -> None:
        self.client = client
        
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
    
    def decode_result(self, result: Any, method: BaleMethod[BaleType]) -> Any:
        result["client_cls"] = self.client
        result["method_data"] = method
        
        model_type = method.__returning__
        return model_type.model_validate(result, context={"client": self.client})
    
    def get_handshake_payload(self) -> bytes:
        request = Request(
            handshake=AuthBody(
                authorized=1,
                ready=1
            )
        )
        
        payload = request.model_dump(by_alias=True, exclude_none=True)
        return self.encoder(payload)
    
    def _get_meta(self) -> dict:
        return {
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
    
    def _get_meta_data(self) -> MetaList:
        data = self._get_meta()
        
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
    
    async def _handle_update(self, update: UpdateBody) -> None:
        event_info = update.body.current_event
        if not event_info:
            return

        event_type, event = event_info
    
        if event_type == "message" and getattr(event, "sender_id", None) == self.client.id:
            return
        
        dp = self.client.dispatcher
        await dp.dispatch(event_type, event)
        
    @abc.abstractmethod
    async def close(self) -> None:
        pass
    
    @abc.abstractmethod
    async def connect(self, token: str) -> None:
        pass
    
    @abc.abstractmethod
    async def handshake_request(self) -> None:
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
