from typing import Optional, Any
from base64 import b64decode

from .session import AiohttpSession, BaseSession
from ..exceptions import AiobaleError
from ..utils import parse_jwt, generate_id
from ..methods import SendMessage, BaleMethod, BaleType
from ..types import (
    Message, 
    MessageContent,
    ClientData,
    Peer,
    Chat,
    TextMessage
)
from ..types.responses import MessagetResponse
from ..enums import ChatType, PeerType


class Client:
    def __init__(
        self,
        token: str,
        session: Optional[BaseSession] = None
    ):
        self.__token = token
        self._me = self._check_token()
        
        if session is None:
            session = AiohttpSession()
            
        self.session = session
        
    @property
    def token(self) -> str:
        return self.__token
    
    @property
    def me(self) -> ClientData:
        return self._me
    
    @property
    def id(self) -> int:
        return self._me.user_id
    
    async def __call__(self, method: BaleMethod[BaleType]):
        return await self.session.make_request(method)
    
    async def start(self) -> None:
        await self.session.connect(self.__token)
    
    def _check_token(self) -> ClientData:
        token = self.__token
        result = parse_jwt(token)
        if not result:
            raise AiobaleError("Not a valid jwt token")
        
        data, _ = result
        if "payload" not in data:
            raise AiobaleError("Wrong jwt payload")
        
        return ClientData.model_validate(data["payload"])
    
    async def send_message(
        self,
        text: str,
        chat_id: int,
        chat_type: ChatType,
        message_id: int | None = None
    ) -> MessagetResponse:
        
        peer_type = self._resolve_peer_type(chat_type)
        peer = Peer(type=peer_type, id=chat_id)
        chat = Chat(type=chat_type, id=chat_id)
        
        message_id = message_id or generate_id()
        
        content = MessageContent(
            text=TextMessage(content=text)
        )
        
        call = SendMessage(
            peer=peer,
            message_id=message_id,
            content=content,
            chat=chat
        )
        
        return await self(call)
        
    def _resolve_peer_type(chat_type: ChatType):
        if chat_type == ChatType.UNKNOWN:
            return PeerType.UNKNOWN
        elif chat_type in (ChatType.PRIVATE, ChatType.BOT):
            return PeerType.PRIVATE
        return PeerType.GROUP
    