from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer, StringValue
from ...types.responses import GroupCreatedResponse
from ...enums import Services, GroupType, Restriction
from ..base import BaleMethod


class CreateGroup(BaleMethod):
    __service__ = Services.GROUPS.value
    __method__ = "CreateGroup"

    __returning__ = GroupCreatedResponse

    random_id: int = Field(..., alias="1")
    title: str = Field(..., alias="2")
    users: Optional[List[ShortPeer]] = Field(None, alias="3")
    group_type: GroupType = Field(GroupType.GROUP, alias="6")
    username: Optional[StringValue] = Field(None, alias="8")
    restriction: Restriction = Field(Restriction.PRIVATE, alias="9")

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            random_id: int,
            title: str,
            users: Optional[List[ShortPeer]],
            group_type: GroupType = GroupType.GROUP,
            username: Optional[StringValue] = None,
            restriction: Restriction = Restriction.PRIVATE,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                random_id=random_id,
                title=title,
                users=users,
                group_type=group_type,
                username=username,
                restriction=restriction,
                **__pydantic_kwargs
            )
