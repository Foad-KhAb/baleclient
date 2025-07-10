from __future__ import annotations

import asyncio
from typing import List, Optional, Any, Type, Final, Union
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
    ValidateCode,
    DeleteMessage,
    ForwardMessages,
    MessageRead
)
from ..types import (
    MessageContent,
    ClientData,
    Peer,
    Chat,
    TextMessage,
    UserAuth,
    IntValue,
    Message,
    InfoMessage
)
from ..types.responses import (
    MessageResponse, 
    PhoneAuthResponse, 
    ValidateCodeResponse,
    DefaultResponse
)
from ..enums import ChatType, PeerType, SendCodeType
from ..dispatcher.dispatcher import Dispatcher
from .auth_cli import PhoneLoginCLI


DEFAULT_SESSION: Final[str] = "./session.bale"


class Client:
    def __init__(
        self,
        dispatcher: Dispatcher,
        session_file: Optional[str] = DEFAULT_SESSION,
        session: Optional[BaseSession] = None
    ):  
        if session is None:
            session = AiohttpSession()
        
        session._bind_client(self)
        self.session = session
        self.dispatcher: Dispatcher = dispatcher
        
        if not isinstance(session_file, str) or not session_file.lower().endswith(".bale"):
            raise AiobaleError(
                f"Invalid session file: {session_file!r}. "
                "Only `.bale` files are allowed."
            )
        
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
        if not self.__session_file:
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
        return await self.session.make_request(method)
    
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
        
        content = await self.session.post(call)
        if not content:
            raise AiobaleError("Invalid code specified.")

        try:
            self._write_session_content(content)
            return self._parse_session_content(content)

        except Exception as e:
            raise AiobaleError("Error while parsing data.") from e

    async def send_message(
        self,
        text: str,
        chat_id: int,
        chat_type: ChatType,
        message_id: int | None = None
    ) -> MessageResponse:
        
        chat = Chat(type=chat_type, id=chat_id)
        peer = self._resolve_peer(chat)
        
        message_id = message_id or generate_id()
        
        content = MessageContent(
            text=TextMessage(value=text)
        )
        
        call = SendMessage(
            peer=peer,
            message_id=message_id,
            content=content,
            chat=chat
        )
        
        return await self(call)
        
    def _resolve_peer_type(self, chat_type: ChatType) -> PeerType:
        if chat_type == ChatType.UNKNOWN:
            return PeerType.UNKNOWN
        elif chat_type in (ChatType.PRIVATE, ChatType.BOT):
            return PeerType.PRIVATE
        return PeerType.GROUP
    
    def _resolve_peer(self, chat: Chat) -> Peer:
        peer_type = self._resolve_peer_type(chat.type)
        return Peer(id=chat.id, type=peer_type)
    
    async def delete_messages(
        self,
        message_ids: List[int],
        message_dates: List[int],
        chat_id: int,
        chat_type: ChatType,
        just_me: Optional[bool] = False
    ) -> DefaultResponse:
        
        if not message_ids or not message_dates:
            raise AiobaleError("`message_ids` or `message_dates` can not be empty")
        
        peer_type = self._resolve_peer_type(chat_type)
        peer = Peer(type=peer_type, id=chat_id)
        
        call = DeleteMessage(
            peer=peer,
            message_ids=message_ids,
            dates=message_dates,
            just_me=IntValue(value=int(just_me))
        )
        
        return await self(call)
    
    async def delete_message(
        self,
        message_id: int,
        message_date: int,
        chat_id: int,
        chat_type: ChatType,
        just_me: Optional[bool] = False
    ) -> DefaultResponse:
        
        return await self.delete_messages(
            message_ids=[message_id],
            message_dates=[message_date],
            chat_id=chat_id,
            chat_type=chat_type,
            just_me=just_me
        )
    
    async def forward_messages(
        self,
        messages: List[Union[Message, InfoMessage]],
        chat_id: int,
        chat_type: ChatType,
        new_ids: Optional[List[int]] = None
    ) -> DefaultResponse:

        if not messages:
            raise AiobaleError("`messages` cannot be empty")

        if new_ids is None:
            new_ids = [generate_id() for _ in messages]

        if len(new_ids) != len(messages):
            raise AiobaleError("Mismatch between number of `new_ids` and `messages`")

        target_peer = Peer(
            type=self._resolve_peer_type(chat_type),
            id=chat_id
        )

        forwarded_messages = [self._ensure_forwarded_message(msg) for msg in messages]

        call = ForwardMessages(
            peer=target_peer,
            message_ids=new_ids,
            forwarded_messages=forwarded_messages
        )

        return await self(call)

    def _ensure_forwarded_message(self, message: Union[Message, InfoMessage]) -> InfoMessage:
        """Ensures that a message is converted to ForwardedMessage if it's not already one."""
        if isinstance(message, InfoMessage):
            return message

        origin_peer = self._resolve_peer(message.chat)

        return InfoMessage(
            peer=origin_peer,
            message_id=message.message_id,
            date=IntValue(value=message.date)
        )
        
    async def forward_message(
        self,
        message: Union[Message, InfoMessage],
        chat_id: int,
        chat_type: ChatType,
        new_id: Optional[int] = None
    ) -> DefaultResponse:
        new_ids = [new_id] if new_id is not None else None

        return await self.forward_messages(
            messages=[message],
            chat_id=chat_id,
            chat_type=chat_type,
            new_ids=new_ids
        )
        
    async def seen_chat(
        self,
        chat_id: int,
        chat_type: ChatType
    ) -> DefaultResponse:
        
        peer_type = self._resolve_peer_type(chat_type)
        peer = Peer(id=chat_id, type=peer_type)
        
        call = MessageRead(
            peer=peer
        )
        
        return await self(call)
