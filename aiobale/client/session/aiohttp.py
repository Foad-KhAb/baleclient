from __future__ import annotations

import aiohttp
import asyncio
from typing import Callable, Any, Optional, Dict, Coroutine, TYPE_CHECKING, Union

from ...methods import BaleMethod, BaleType
from ...types import Response
from ...utils import add_header, clean_grpc
from ...exceptions import BaleError, AiobaleError
from .base import BaseSession

if TYPE_CHECKING:
    from ..client import Client


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/135.0.0.0 Safari/537.36"
)


class AiohttpSession(BaseSession):
    def __init__(
        self,
        user_agent: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.session = None
        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self._running = False

        self.user_agent = user_agent or DEFAULT_USER_AGENT

        self.handlers: Dict[str, Callable[[dict], Coroutine]] = {}
        self._pending_requests: Dict[int, asyncio.Future] = {}

    def add_handler(self, message_type: str, handler: Callable[[dict], Coroutine]):
        self.handlers[message_type] = handler

    def _build_headers(self, token: str) -> Dict[str, str]:
        return {
            "User-Agent": self.user_agent,
            "Cookie": f"access_token={token}"
        }

    async def connect(self, token: str):
        if not self.session:
            self.session = aiohttp.ClientSession()
            
        if self._running:
            raise AiobaleError("Client is already running")
        
        headers = self._build_headers(token)
        self.ws = await self.session.ws_connect(
            self.ws_url,
            timeout=self.timeout,
            headers=headers,
            origin="https://web.bale.ai"
        )
        self._running = True

    async def _listen(self):
        try:
            async for msg in self.ws:
                if msg.type != aiohttp.WSMsgType.BINARY:
                    continue
                
                try:
                    data = self.decoder(msg.data)
                    received = Response.model_validate(data, context={"client": self.client})
                except:
                    continue
                
                if received.update is not None:
                    asyncio.create_task(self._handle_update(received.update.body))
                    continue

                response = received.response
                if response is None:
                    continue

                future = self._pending_requests.pop(response.number, None)
                if future is None or future.done():
                    continue

                if response.error:
                    raise BaleError(response.error.message, response.error.topic)

                future.set_result(response.result)

        except Exception as e:
            print(f"WebSocket listening failed: {e}")
        finally:
            self._running = False

    async def make_request(
        self,
        method: BaleMethod[BaleType],
        timeout: Optional[int] = None,
    ) -> BaleType:
        if not self.ws:
            raise RuntimeError("WebSocket is not connected")

        request_id = self._next_request_id()
        payload = self.build_payload(method, request_id)

        future = asyncio.get_event_loop().create_future()
        self._pending_requests[request_id] = future
        await self.ws.send_bytes(payload)

        try:
            result = await asyncio.wait_for(future, timeout=timeout or self.timeout)
            return self.decode_result(result, method)
        
        except asyncio.TimeoutError:
            self._pending_requests.pop(request_id, None)
            raise 
        
    async def handshake_request(self):
        payload = self.get_handshake_payload()
        await self.ws.send_bytes(payload)
        
    async def post(self, method: BaleMethod[BaleType]) -> Union[bytes, BaleType]:
        if not self.session:
            self.session = aiohttp.ClientSession()
            
        headers = {
            'User-Agent': self.user_agent,
            'Origin': "https://web.bale.ai",
            'content-type': "application/grpc-web+proto"
        }
        headers.update({k[0].upper() + k[1:]: v for k, v in self._get_meta().items()})

        url = f"{self.post_url}/{method.__service__}/{method.__method__}"
        data = method.model_dump(by_alias=True)
        payload = add_header(self.encoder(data))
        
        req = await self.session.post(url=url, headers=headers, data=payload)
        content = await req.read()
        
        if method.__returning__ is None:
            return content
        
        result = self.decoder(clean_grpc(content))
        return method.__returning__.model_validate(result)

    async def close(self):
        self._running = False
        if self.ws:
            await self.ws.close()
        await self.session.close()
