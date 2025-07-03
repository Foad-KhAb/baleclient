import aiohttp
import asyncio
from typing import Callable, Any, Optional, Dict, Coroutine

from ...methods import BaleMethod, BaleType
from ..client import Client
from ...types import Response
from ...exceptions import BaleError
from .base import BaseSession


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/135.0.0.0 Safari/537.36"
)


class AiohttpSession(BaseSession):
    def __init__(
        self,
        ws_url: str = BaseSession.ws_url,
        decoder: Callable[..., Any] = BaseSession.decoder,
        encoder: Callable[..., dict] = BaseSession.encoder,
        timeout: float = BaseSession.timeout,
        user_agent: Optional[str] = None,
    ) -> None:
        super().__init__(ws_url, decoder, encoder, timeout)
        self.session = aiohttp.ClientSession()
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
        headers = self._build_headers(token)
        self.ws = await self.session.ws_connect(
            self.ws_url,
            timeout=self.timeout,
            headers=headers,
        )
        self._running = True
        asyncio.create_task(self._listen())

    async def _listen(self):
        try:
            async for msg in self.ws:
                if msg.type != aiohttp.WSMsgType.BINARY:
                    continue
                
                try:
                    data = self.decoder(msg.data)
                    received = Response.model_validate(data)
                except:
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
            return self.decode_result(result, method, client)
        
        except asyncio.TimeoutError:
            self._pending_requests.pop(request_id, None)
            raise 

    async def close(self):
        self._running = False
        if self.ws:
            await self.ws.close()
        await self.session.close()
