import aiohttp
import asyncio
from typing import Callable, Any, Optional, Dict, Coroutine

from ...methods import BaleMethod, BaleType
from ..client import Client
from .base import BaseSession


class AiohttpSession(BaseSession):
    def __init__(
        self,
        ws_url: str = BaseSession.ws_url,
        decoder: Callable[..., Any] = BaseSession.decoder,
        encoder: Callable[..., dict] = BaseSession.encoder,
        timeout: float = BaseSession.timeout,
    ) -> None:
        super().__init__(ws_url, decoder, encoder, timeout)
        self.session = aiohttp.ClientSession()
        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self._running = False

        self.handlers: Dict[str, Callable[[dict], Coroutine]] = {}
        self._pending_requests: Dict[int, asyncio.Future] = {}

    def add_handler(self, message_type: str, handler: Callable[[dict], Coroutine]):
        self.handlers[message_type] = handler

    async def connect(self):
        self.ws = await self.session.ws_connect(self.ws_url, timeout=self.timeout)
        self._running = True
        asyncio.create_task(self._listen())

    async def _listen(self):
        try:
            async for msg in self.ws:
                if msg.type == aiohttp.WSMsgType.BINARY:
                    data = self.decoder(msg.data)
                    request_id = data.get("request_id")

                    if request_id and request_id in self._pending_requests:
                        future = self._pending_requests.pop(request_id)
                        if not future.done():
                            future.set_result(data)
                    else:
                        msg_type = data.get("type")
                        handler = self.handlers.get(msg_type)
                        if handler:
                            await handler(data)
        except Exception as e:
            print("WS listen error:", e)
        finally:
            self._running = False

    async def make_request(
        self,
        client: Client,
        method: BaleMethod[BaleType],
        timeout: Optional[int] = None,
    ) -> BaleType:
        if not self.ws:
            raise RuntimeError("WebSocket is not connected")

        request_id = self.next_request_number()
        payload = self.build_payload(method, request_id)

        future = asyncio.get_event_loop().create_future()
        self._pending_requests[request_id] = future
        await self.ws.send_bytes(payload)

        try:
            result = await asyncio.wait_for(future, timeout=timeout or self.timeout)
            return self.decode_result(result)
        
        except asyncio.TimeoutError:
            self._pending_requests.pop(request_id, None)
            raise 

    async def close(self):
        self._running = False
        if self.ws:
            await self.ws.close()
        await self.session.close()
