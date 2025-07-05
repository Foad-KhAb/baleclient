from __future__ import annotations

import asyncio
from typing import Optional, Any, Type, Final
from types import TracebackType
import os

from .session import AiohttpSession, BaseSession
from ..exceptions import AiobaleError
from ..utils import parse_jwt, generate_id, clean_grpc
from ..methods import (
    SendMessage, 
    BaleMethod, 
    BaleType,
    StartPhoneAuth,
    ValidateCode
)
from ..types import (
    MessageContent,
    ClientData,
    Peer,
    Chat,
    TextMessage,
    UserAuth
)
from ..types.responses import MessageResponse, PhoneAuthResponse, ValidateCodeResponse
from ..enums import ChatType, PeerType, SendCodeType
from .auth_cli import PhoneLoginCLI


DEFAULT_SESSION: Final[str] = "./session.abl"


class Client:
    def __init__(
        self,
        session_file: Optional[str] = DEFAULT_SESSION,
        session: Optional[BaseSession] = None
    ):  
        if session is None:
            session = AiohttpSession()
            
        self.session = session
        
        self.__session_file = session_file
        self.__token = None
        self._me = None
        
        self._add_token_via_file()
        
    @property
    def token(self) -> str:
        return self.__token
    
    @property
    def me(self) -> ClientData:
        return self._me
    
    @property
    def id(self) -> int:
        return self._me.id
    
    def _write_session_content(self, content: bytes) -> None:
        if not self.__session_file or os.path.exists(self.__session_file):
            return
        
        with open(self.__session_file, "wb") as f:
            f.write(content)
    
    def _get_session_content(self) -> Optional[bytes]:
        if self.__session_file and os.path.exists(self.__session_file):
            with open(self.__session_file, "rb") as f:
                return f.read()
        return None

    def _parse_session_content(self, data: bytes) -> ValidateCodeResponse:
        decoded = self.session.decoder(clean_grpc(data))
        model = ValidateCodeResponse.model_validate(decoded)
        
        self.__token = model.jwt.value
        self._me = self._check_token(model.user)
        
        return model
    
    def _add_token_via_file(self) -> bool:
        content = self._get_session_content()
        if content is None:
            return False
        
        self._parse_session_content(content)
        return True
    
    async def __call__(self, method: BaleMethod[BaleType]):
        return await self.session.make_request(self, method)
    
    async def start(self, run_in_background: bool = False) -> None:
        if self.__token is None:
            if not self._add_token_via_file():
                auth_cli = PhoneLoginCLI(self)
                await auth_cli.start()
            
        await self.session.connect(self.__token)
        await self.session.login_request()

        if run_in_background:
            asyncio.create_task(self.session._listen())
        else:
            await self.session._listen()
            
    async def stop(self):
        await self.session.close()
        
    async def __aenter__(self) -> Client:
        await self.start(True)
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.session.close()
    
    def _check_token(self, user: UserAuth) -> ClientData:
        token = self.__token
        result = parse_jwt(token)
        if not result:
            raise AiobaleError("Not a valid jwt token")
        
        data, _ = result
        if "payload" not in data:
            raise AiobaleError("Wrong jwt payload")
        
        data["payload"]["user"] = user
        return ClientData.model_validate(data["payload"])
    
    async def login(
        self, 
        phone_number: int,
        code_type: Optional[SendCodeType] = SendCodeType.DEFAULT
    ) -> PhoneAuthResponse:
        call = StartPhoneAuth(
            phone_number=phone_number,
            app_id=4,
            app_key="C28D46DC4C3A7A26564BFCC48B929086A95C93C98E789A19847BEE8627DE4E7D",
            device_hash="ce5ced83-a9ab-47fa-80c8-ed425eeb2ace",
            device_title="Chrome_138.0.0.0, Windows",
            send_code_type=code_type
        )
        
        try:
            return await self.session.post(call)
        except:
            raise AiobaleError("This phone number is banned")
        
    async def validate_code(
        self,
        code: str,
        transaction_hash: str
    ) -> ValidateCodeResponse:
        call = ValidateCode(
            code=code,
            transaction_hash=transaction_hash
        )
        
        try:
            content = await self.session.post(call)
            self._write_session_content(content)
            
            return self._parse_session_content(content)
        
        except:
            raise AiobaleError("wrong code specified")
    
    async def send_message(
        self,
        text: str,
        chat_id: int,
        chat_type: ChatType,
        message_id: int | None = None
    ) -> MessageResponse:
        
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
        
    def _resolve_peer_type(self, chat_type: ChatType):
        if chat_type == ChatType.UNKNOWN:
            return PeerType.UNKNOWN
        elif chat_type in (ChatType.PRIVATE, ChatType.BOT):
            return PeerType.PRIVATE
        return PeerType.GROUP
