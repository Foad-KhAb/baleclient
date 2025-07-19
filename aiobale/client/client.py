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
    StopTyping,
    Typing,
    GetParameters,
    EditParameter,
    GetMessagesReactions,
    GetMessageReactionsList,
    MessageSetReaction,
    MessageRemoveReaction,
    GetMessagesViews,
    ValidatePassword,
    GetFullGroup,
    LoadMembers,
    CreateGroup,
    InviteUsers,
    EditGroupTitle,
    EditGroupAbout,
    SetRestriction,
    GetGroupInviteURL,
    RevokeInviteURL,
    LeaveGroup,
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
    ExtKeyValue,
    MessageReactions,
    ReactionData,
    Reaction,
    MessageViews,
    FullGroup,
    ShortPeer,
    Member,
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
    ParametersResponse,
    ReactionsResponse,
    ReactionListResponse,
    ReactionSentResponse,
    ViewsResponse,
    FullGroupResponse,
    MembersResponse,
    GroupCreatedResponse,
    InviteResponse,
    InviteURLResponse,
)
from ..enums import (
    ChatType,
    PeerType,
    SendCodeType,
    ListLoadMode,
    PeerSource,
    ReportKind,
    TypingMode,
    Restriction,
    GroupType,
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
        if isinstance(content, str):
            match content:
                case "PHONE_CODE_INVALID":
                    raise AiobaleError("Invalid code specified.")
                case "password needed for login":
                    raise AiobaleError("Password needed for login")
                case _:
                    raise AiobaleError("Unknown Error")

        try:
            self._write_session_content(content)
            return self._parse_session_content(content)

        except Exception as e:
            raise AiobaleError("Error while parsing data.") from e

    async def validate_password(
        self, password: str, transaction_hash: str
    ) -> ValidateCodeResponse:
        call = ValidatePassword(password=password, transaction_hash=transaction_hash)

        content = await self.session.post(call)
        if isinstance(content, str):
            match content:
                case "wrong password":
                    raise AiobaleError("Wrong password specified.")
                case _:
                    raise AiobaleError("Unknown Error")

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
        self,
        message: Union[Message, InfoMessage, OtherMessage],
        seq: Optional[int] = None,
    ) -> InfoMessage:
        """Ensures that a message is converted to OtherMessage if it's not already one."""
        if isinstance(message, OtherMessage):
            if seq is not None:
                message.seq = seq

            return message

        return OtherMessage(message_id=message.message_id, date=message.date, seq=seq)

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
            kind=kind,
        )

    async def start_typing(
        self,
        chat_id: int,
        chat_type: ChatType,
        typing_mode: TypingMode = TypingMode.TEXT,
    ) -> DefaultResponse:
        call = Typing(peer=Peer(id=chat_id, type=chat_type), typing_type=typing_mode)
        return await self(call)

    async def stop_typing(
        self,
        chat_id: int,
        chat_type: ChatType,
        typing_mode: TypingMode = TypingMode.TEXT,
    ) -> DefaultResponse:
        call = StopTyping(
            peer=Peer(id=chat_id, type=chat_type), typing_type=typing_mode
        )
        return await self(call)

    async def get_parameters(self) -> List[ExtKeyValue]:
        call = GetParameters()
        result: ParametersResponse = await self(call)
        return result.params

    async def edit_parameter(self, key: str, value: str) -> DefaultResponse:
        call = EditParameter(key=key, value=value)
        return await self(call)

    async def get_messages_reactions(
        self,
        messages: List[Union[Message, InfoMessage, OtherMessage]],
        chat_id: int,
        chat_type: ChatType,
    ) -> List[MessageReactions]:
        other_messages = [self._ensure_other_message(message) for message in messages]
        peer = Peer(id=chat_id, type=chat_type)

        call = GetMessagesReactions(
            peer=peer,
            message_ids=other_messages,
            origin_peer=peer,
            origin_message_ids=other_messages,
        )
        result: ReactionsResponse = await self(call)
        return result.messages

    async def get_message_reactions(
        self,
        message: Union[Message, InfoMessage, OtherMessage],
        chat_id: int,
        chat_type: ChatType,
    ) -> Optional[MessageReactions]:
        result = await self.get_messages_reactions(
            messages=[message], chat_id=chat_id, chat_type=chat_type
        )
        return result[0] if result else None

    async def get_reaction_list(
        self,
        emojy: str,
        message: Union[Message, InfoMessage, OtherMessage],
        chat_id: int,
        chat_type: ChatType,
        page: int = 1,
        limit: int = 20,
    ) -> List[ReactionData]:
        peer = Peer(id=chat_id, type=chat_type)
        call = GetMessageReactionsList(
            peer=peer,
            message_id=message.message_id,
            date=message.date,
            emojy=emojy,
            page=page,
            limit=limit,
        )
        result: ReactionListResponse = await self(call)
        return result.data

    async def set_reaction(
        self,
        emojy: str,
        message: Union[Message, InfoMessage, OtherMessage],
        chat_id: int,
        chat_type: ChatType,
    ) -> List[Reaction]:
        peer = Peer(id=chat_id, type=chat_type)
        call = MessageSetReaction(
            peer=peer, message_id=message.message_id, date=message.date, emojy=emojy
        )
        result: ReactionSentResponse = await self(call)
        return result.reactions

    async def remove_reaction(
        self,
        emojy: str,
        message: Union[Message, InfoMessage, OtherMessage],
        chat_id: int,
        chat_type: ChatType,
    ) -> List[Reaction]:
        peer = Peer(id=chat_id, type=chat_type)
        call = MessageRemoveReaction(
            peer=peer, message_id=message.message_id, date=message.date, emojy=emojy
        )
        result: ReactionSentResponse = await self(call)
        return result.reactions

    async def get_messages_views(
        self, messages: List[Union[Message, InfoMessage, OtherMessage]], chat_id: int
    ) -> List[MessageViews]:
        other_messages = [self._ensure_other_message(message) for message in messages]
        peer = Peer(id=chat_id, type=2)

        call = GetMessagesViews(peer=peer, message_ids=other_messages)
        result: ViewsResponse = await self(call)
        return result.messages

    async def get_message_views(
        self, message: Union[Message, InfoMessage, OtherMessage], chat_id: int
    ) -> List[MessageViews]:
        return await self.get_messages_views(messages=[message], chat_id=chat_id)

    async def get_full_group(self, chat_id: int) -> FullGroup:
        peer = ShortPeer(id=chat_id)
        call = GetFullGroup(group=peer)

        result: FullGroupResponse = await self(call)
        return result.fullgroup

    async def load_members(
        self, chat_id: int, limit: int = 20, next: Optional[int] = None
    ) -> List[Member]:
        peer = ShortPeer(id=chat_id)
        call = LoadMembers(group=peer, limit=limit, next=next)

        result: MembersResponse = await self(call)
        return result.members

    async def create_group(
        self,
        title: str,
        username: Optional[str] = None,
        users: Tuple[int] = (),
        group_type: GroupType = GroupType.GROUP,
    ) -> GroupCreatedResponse:
        random_id = generate_id()
        users = [ShortPeer(id=v) for v in users]
        restriction = Restriction.PUBLIC if username else Restriction.PRIVATE

        call = CreateGroup(
            random_id=random_id,
            title=title,
            users=users,
            username=StringValue(value=username),
            group_type=group_type,
            restriction=restriction,
        )

        return await self(call)

    async def create_channel(
        self, title: str, username: Optional[str] = None, users: Tuple[int] = ()
    ) -> GroupCreatedResponse:
        return await self.create_group(
            title=title, username=username, users=users, group_type=GroupType.CHANNEL
        )

    async def invite_users(self, users: Tuple[int], chat_id: int) -> InviteResponse:
        call = InviteUsers(
            group=ShortPeer(id=chat_id),
            random_id=generate_id(12),
            users=[ShortPeer(id=u) for u in users],
        )
        return await self(call)

    async def edit_group_title(self, title: str, chat_id: int) -> DefaultResponse:
        call = EditGroupTitle(
            group=ShortPeer(id=chat_id), random_id=generate_id(12), title=title
        )
        return await self(call)

    async def edit_group_about(self, about: str, chat_id: int) -> DefaultResponse:
        call = EditGroupAbout(
            group=ShortPeer(id=chat_id),
            random_id=generate_id(12),
            about=StringValue(value=about),
        )
        return await self(call)

    async def make_group_public(self, chat_id: int, username: str) -> DefaultResponse:
        call = SetRestriction(
            group=ShortPeer(id=chat_id),
            restriction=Restriction.PUBLIC,
            username=StringValue(value=username),
        )
        return await self(call)

    async def make_group_private(self, chat_id: int) -> DefaultResponse:
        call = SetRestriction(
            group=ShortPeer(id=chat_id), restriction=Restriction.PRIVATE
        )
        return await self(call)

    async def get_invite_link(self, chat_id: int) -> str:
        call = GetGroupInviteURL(group=ShortPeer(id=chat_id))
        result: InviteURLResponse = await self(call)
        return result.url

    async def revoke_invite_link(self, chat_id: int) -> str:
        call = RevokeInviteURL(group=ShortPeer(id=chat_id))
        result: InviteURLResponse = await self(call)
        return result.url

    async def leave_group(self, chat_id: int) -> DefaultResponse:
        call = LeaveGroup(group=ShortPeer(id=chat_id), random_id=generate_id(12))
        return await self(call)
