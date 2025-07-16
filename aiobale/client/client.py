from __future__ import annotations

import asyncio
from typing import Dict, List, Optional, Any, Tuple, Type, Final, Union
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
    MessageRead,
    EditName,
    EditNickName,
    CheckNickName,
    UpdateMessage,
    ClearChat,
    DeleteChat,
    LoadHistory,
    SetOnline,
    PinMessage,
    UnPinMessages,
    LoadPinnedMessages,
    LoadDialogs,
    EditAbout,
    LoadFullUsers,
    LoadUsers,
    EditUserLocalName,
    BlockUser,
    UnblockUser,
    LoadBlockedUsers,
    SearchContact,
    ImportContacts,
    ResetContacts,
    RemoveContact,
    AddContact,
    GetContacts,
    SendReport,
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
    InfoMessage,
    StringValue,
    OtherMessage,
    MessageData,
    QuotedMessage,
    PeerData,
    InfoPeer,
    FullUser,
    User,
    ContactData,
    Report,
    PeerReport,
    MessageReport,
)
from ..types.responses import (
    MessageResponse,
    PhoneAuthResponse,
    ValidateCodeResponse,
    DefaultResponse,
    NickNameAvailable,
    HistoryResponse,
    DialogResponse,
    FullUsersResponse,
    UsersResponse,
    BlockedUsersResponse,
    ContactResponse,
    ContactsResponse,
)
from ..enums import (
    ChatType,
    PeerType,
    SendCodeType,
    ListLoadMode,
    PeerSource,
    ReportKind,
)
from ..dispatcher.dispatcher import Dispatcher
from .auth_cli import PhoneLoginCLI


DEFAULT_SESSION: Final[str] = "./session.bale"


class Client:
    def __init__(
        self,
        dispatcher: Dispatcher,
        session_file: Optional[str] = DEFAULT_SESSION,
        session: Optional[BaseSession] = None,
    ):
        if session is None:
            session = AiohttpSession()

        session._bind_client(self)
        self.session = session
        self.dispatcher: Dispatcher = dispatcher

        if not isinstance(session_file, str) or not session_file.lower().endswith(
            ".bale"
        ):
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
        await self.session.handshake_request()

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
        code_type: Optional[SendCodeType] = SendCodeType.DEFAULT,
    ) -> PhoneAuthResponse:
        call = StartPhoneAuth(
            phone_number=phone_number,
            app_id=4,
            app_key="C28D46DC4C3A7A26564BFCC48B929086A95C93C98E789A19847BEE8627DE4E7D",
            device_hash="ce5ced83-a9ab-47fa-80c8-ed425eeb2ace",
            device_title="Chrome_138.0.0.0, Windows",
            send_code_type=code_type,
        )

        try:
            return await self.session.post(call)
        except:
            raise AiobaleError("This phone number is banned")

    async def validate_code(
        self, code: str, transaction_hash: str
    ) -> ValidateCodeResponse:
        call = ValidateCode(code=code, transaction_hash=transaction_hash)

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
        reply_to: Optional[Union[Message, InfoMessage]] = None,
        message_id: Optional[int] = None,
    ) -> Message:
        chat = Chat(type=chat_type, id=chat_id)
        peer = self._resolve_peer(chat)

        message_id = message_id or generate_id()

        content = MessageContent(text=TextMessage(value=text))

        if reply_to is not None:
            reply_to = self._ensure_info_message(reply_to)

        call = SendMessage(
            peer=peer,
            message_id=message_id,
            content=content,
            reply_to=reply_to,
            chat=chat,
        )

        result: MessageResponse = await self(call)
        return result.message

    def _resolve_peer_type(self, chat_type: ChatType) -> PeerType:
        if chat_type == ChatType.UNKNOWN:
            return PeerType.UNKNOWN
        elif chat_type in (ChatType.PRIVATE, ChatType.BOT):
            return PeerType.PRIVATE
        return PeerType.GROUP

    def _resolve_peer(self, chat: Chat) -> Peer:
        peer_type = self._resolve_peer_type(chat.type)
        return Peer(id=chat.id, type=peer_type)

    async def edit_message(
        self, text: str, message_id: int, chat_id: int, chat_type: ChatType
    ) -> DefaultResponse:
        peer_type = self._resolve_peer_type(chat_type)
        peer = Peer(type=peer_type, id=chat_id)
        content = MessageContent(text=TextMessage(value=text))

        call = UpdateMessage(peer=peer, message_id=message_id, updated_message=content)

        return await self(call)

    async def delete_messages(
        self,
        message_ids: List[int],
        message_dates: List[int],
        chat_id: int,
        chat_type: ChatType,
        just_me: Optional[bool] = False,
    ) -> DefaultResponse:
        if not message_ids or not message_dates:
            raise AiobaleError("`message_ids` or `message_dates` can not be empty")

        peer_type = self._resolve_peer_type(chat_type)
        peer = Peer(type=peer_type, id=chat_id)

        call = DeleteMessage(
            peer=peer,
            message_ids=message_ids,
            dates=message_dates,
            just_me=IntValue(value=int(just_me)),
        )

        return await self(call)

    async def delete_message(
        self,
        message_id: int,
        message_date: int,
        chat_id: int,
        chat_type: ChatType,
        just_me: Optional[bool] = False,
    ) -> DefaultResponse:
        return await self.delete_messages(
            message_ids=[message_id],
            message_dates=[message_date],
            chat_id=chat_id,
            chat_type=chat_type,
            just_me=just_me,
        )

    async def forward_messages(
        self,
        messages: List[Union[Message, InfoMessage]],
        chat_id: int,
        chat_type: ChatType,
        new_ids: Optional[List[int]] = None,
    ) -> DefaultResponse:
        if not messages:
            raise AiobaleError("`messages` cannot be empty")

        if new_ids is None:
            new_ids = [generate_id() for _ in messages]

        if len(new_ids) != len(messages):
            raise AiobaleError("Mismatch between number of `new_ids` and `messages`")

        target_peer = Peer(type=self._resolve_peer_type(chat_type), id=chat_id)

        forwarded_messages = [self._ensure_info_message(msg) for msg in messages]

        call = ForwardMessages(
            peer=target_peer, message_ids=new_ids, forwarded_messages=forwarded_messages
        )

        return await self(call)

    def _ensure_info_message(self, message: Union[Message, InfoMessage]) -> InfoMessage:
        """Ensures that a message is converted to InfoMessage if it's not already one."""
        if isinstance(message, InfoMessage):
            return message

        origin_peer = self._resolve_peer(message.chat)

        return InfoMessage(
            peer=origin_peer,
            message_id=message.message_id,
            date=IntValue(value=message.date),
        )
        
    def _ensure_other_message(
        self, message: Union[Message, InfoMessage, OtherMessage], seq: Optional[int] = None
    ) -> InfoMessage:
        """Ensures that a message is converted to OtherMessage if it's not already one."""
        if isinstance(message, OtherMessage):
            if seq is not None:
                message.seq = seq
            
            return message

        return OtherMessage(
            message_id=message.message_id,
            data=message.data,
            seq=seq
        )

    async def forward_message(
        self,
        message: Union[Message, InfoMessage],
        chat_id: int,
        chat_type: ChatType,
        new_id: Optional[int] = None,
    ) -> DefaultResponse:
        new_ids = [new_id] if new_id is not None else None

        return await self.forward_messages(
            messages=[message], chat_id=chat_id, chat_type=chat_type, new_ids=new_ids
        )

    async def seen_chat(self, chat_id: int, chat_type: ChatType) -> DefaultResponse:
        peer_type = self._resolve_peer_type(chat_type)
        peer = Peer(id=chat_id, type=peer_type)

        call = MessageRead(peer=peer)

        return await self(call)

    async def clear_chat(self, chat_id: int, chat_type: ChatType) -> DefaultResponse:
        peer_type = self._resolve_peer_type(chat_type)
        peer = Peer(id=chat_id, type=peer_type)

        call = ClearChat(peer=peer)

        return await self(call)

    async def delete_chat(self, chat_id: int, chat_type: ChatType) -> DefaultResponse:
        peer_type = self._resolve_peer_type(chat_type)
        peer = Peer(id=chat_id, type=peer_type)

        call = DeleteChat(peer=peer)

        return await self(call)

    async def load_history(
        self,
        chat_id: int,
        chat_type: ChatType,
        limit: int = 20,
        offset_date: int = -1,
        load_mode: ListLoadMode = ListLoadMode.BACKWARD,
    ) -> List[Message]:
        chat = Chat(id=chat_id, type=chat_type)
        peer = self._resolve_peer(chat)

        call = LoadHistory(
            peer=peer, offset_date=offset_date, load_mode=load_mode, limit=limit
        )

        result: HistoryResponse = await self(call)
        result.add_chat(chat)

        return self._resolve_list_messages(result.data)

    @staticmethod
    def _resolve_list_messages(
        data: List[Union[MessageData, QuotedMessage]],
    ) -> List[Message]:
        return [item.message for item in data]

    async def pin_message(
        self,
        message_id: int,
        message_date: int,
        chat_id: int,
        chat_type: ChatType,
        just_me: bool = False,
    ) -> DefaultResponse:
        chat = Chat(id=chat_id, type=chat_type)
        peer = self._resolve_peer(chat)

        call = PinMessage(
            peer=peer,
            message=OtherMessage(message_id=message_id, date=message_date),
            just_me=just_me,
        )

        return await self(call)

    async def unpin_message(
        self, message_id: int, message_date: int, chat_id: int, chat_type: ChatType
    ) -> DefaultResponse:
        chat = Chat(id=chat_id, type=chat_type)
        peer = self._resolve_peer(chat)

        call = UnPinMessages(
            peer=peer, messages=[OtherMessage(message_id=message_id, date=message_date)]
        )

        return await self(call)

    async def unpin_all(
        self,
        one_message_id: int,
        one_message_date: int,
        chat_id: int,
        chat_type: ChatType,
    ) -> DefaultResponse:
        chat = Chat(id=chat_id, type=chat_type)
        peer = self._resolve_peer(chat)

        call = UnPinMessages(
            peer=peer,
            messages=[OtherMessage(message_id=one_message_id, date=one_message_date)],
            all_messages=True,
        )

        return await self(call)

    async def load_pinned_messages(
        self, chat_id: int, chat_type: ChatType
    ) -> List[Message]:
        chat = Chat(id=chat_id, type=chat_type)
        peer = self._resolve_peer(chat)

        call = LoadPinnedMessages(peer=peer)

        result: HistoryResponse = await self(call)
        result.add_chat(chat)

        return self._resolve_list_messages(result.data)

    async def load_dialogs(
        self, limit: int = 40, offset_date: int = -1, exclude_pinned: bool = False
    ) -> List[PeerData]:
        call = LoadDialogs(
            offset_date=offset_date, limit=limit, exclude_pinned=exclude_pinned
        )

        result: DialogResponse = await self(call)
        return result.dialogs

    async def edit_name(self, name: str) -> DefaultResponse:
        call = EditName(name=name)
        return await self(call)

    async def check_username(self, username: str) -> bool:
        call = CheckNickName(nick_name=username)

        result: NickNameAvailable = await self(call)
        return result.availbale

    async def edit_username(self, username: str) -> DefaultResponse:
        call = EditNickName(nick_name=StringValue(value=username))
        return await self(call)

    async def edit_about(self, about: str) -> DefaultResponse:
        call = EditAbout(about=StringValue(value=about))
        return await self(call)

    async def load_full_users(
        self, peers: List[Union[Peer, InfoPeer]]
    ) -> List[FullUser]:
        peers = [
            InfoPeer(id=peer.id, type=peer.type) if isinstance(peer, Peer) else peer
            for peer in peers
        ]

        call = LoadFullUsers(peers=peers)

        result: FullUsersResponse = await self(call)
        return result.data

    async def load_full_user(self, chat_id: int, chat_type: ChatType) -> FullUser:
        peers = [InfoPeer(id=chat_id, type=chat_type)]
        result = await self.load_full_users(peers=peers)
        return result[0]

    async def get_full_me(self) -> FullUser:
        peers = [InfoPeer(id=self.id, type=ChatType.PRIVATE)]
        result = await self.load_full_users(peers=peers)
        return result[0]

    async def load_users(self, peers: List[Union[Peer, InfoPeer]]) -> List[User]:
        peers = [
            InfoPeer(id=peer.id, type=peer.type) if isinstance(peer, Peer) else peer
            for peer in peers
        ]

        call = LoadUsers(peers=peers)

        result: UsersResponse = await self(call)
        return result.data

    async def load_user(self, chat_id: int, chat_type: ChatType) -> User:
        peers = [InfoPeer(id=chat_id, type=chat_type)]
        result = await self.load_users(peers=peers)
        return result[0]

    async def get_me(self) -> FullUser:
        peers = [InfoPeer(id=self.id, type=ChatType.PRIVATE)]
        result = await self.load_users(peers=peers)
        return result[0]

    async def edit_user_local_name(
        self, name: str, user_id: int, access_hash: int = 1
    ) -> DefaultResponse:
        call = EditUserLocalName(user_id=user_id, name=name, access_hash=access_hash)

        return await self(call)

    async def block_user(self, user_id: int) -> DefaultResponse:
        info_peer = InfoPeer(id=user_id, type=ChatType.PRIVATE)
        call = BlockUser(peer=info_peer)

        return await self(call)

    async def unblock_user(self, user_id: int) -> DefaultResponse:
        info_peer = InfoPeer(id=user_id, type=ChatType.PRIVATE)
        call = UnblockUser(peer=info_peer)

        return await self(call)

    async def load_blocked_users(self) -> List[InfoPeer]:
        call = LoadBlockedUsers()
        result: BlockedUsersResponse = await self(call)
        return result.users

    async def load_contacts(self) -> List[InfoPeer]:
        call = GetContacts()
        result: BlockedUsersResponse = await self(call)
        return result.users

    async def search_contact(self, phone_number: str) -> Optional[InfoPeer]:
        phone_number = phone_number.replace("+", "")
        call = SearchContact(request=phone_number)

        result: ContactResponse = await self(call)
        return result.user

    async def search_username(self, username: str) -> ContactResponse:
        call = SearchContact(request=username)
        return await self(call)

    async def import_contacts(self, contacts: List[Tuple[int, str]]) -> List[InfoPeer]:
        contacts = [
            ContactData(phone_number=contact[0], name=StringValue(value=contact[1]))
            for contact in contacts
        ]

        call = ImportContacts(phones=contacts)
        result: ContactsResponse = await self(call)
        return result.peers

    async def reset_contacts(self) -> DefaultResponse:
        call = ResetContacts()
        return await self(call)

    async def remove_contact(self, user_id: int) -> DefaultResponse:
        call = RemoveContact(user_id=user_id)
        return await self(call)

    async def add_contact(self, user_id: int) -> DefaultResponse:
        call = AddContact(user_id=user_id)
        return await self(call)

    async def set_online(self, is_online: bool, timeout: int) -> DefaultResponse:
        call = SetOnline(is_online=is_online, timeout=timeout)
        return await self(call)

    async def report_chat(
        self,
        chat_id: int,
        chat_type: ChatType,
        reason: Optional[str] = None,
        kind: ReportKind = ReportKind.SPAM,
    ) -> DefaultResponse:
        peer_report = PeerReport(
            source=PeerSource.DIALOGS, peer=Peer(id=chat_id, type=chat_type)
        )
        report = Report(kind=kind, description=reason, peer_report=peer_report)
        call = SendReport(report_body=report)
        return await self(call)

    async def report_messages(
        self,
        chat_id: int,
        chat_type: ChatType,
        messages: List[Union[Message, InfoMessage, OtherMessage]],
        reason: Optional[str] = None,
        kind: ReportKind = ReportKind.SPAM,
    ) -> DefaultResponse:
        other_messages = [self._ensure_other_message(message) for message in messages]
        
        message_report = MessageReport(
            messages=other_messages, peer=Peer(id=chat_id, type=chat_type)
        )
        report = Report(kind=kind, description=reason, message_report=message_report)
        call = SendReport(report_body=report)
        return await self(call)
    
    async def report_message(
        self,
        chat_id: int,
        chat_type: ChatType,
        message: Union[Message, InfoMessage, OtherMessage],
        reason: Optional[str] = None,
        kind: ReportKind = ReportKind.SPAM,
    ) -> DefaultResponse:
        return await self.report_messages(
            chat_id=chat_id,
            chat_type=chat_type,
            messages=[message],
            reason=reason,
            kind=kind
        )
