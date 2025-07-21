from __future__ import annotations

from pydantic import Field
from typing import Optional, Union, TYPE_CHECKING, List, Dict

from .base import BaleObject


class TextMessage(BaleObject):
    """
    Represents a plain text message content.

    Attributes:
        value: The actual text content of the message.
    """

    value: str = Field(..., alias="1")
    """The textual content of the message."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            value: str,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(value=value, **__pydantic_kwargs)


class MessageCaption(BaleObject):
    """
    Represents an optional caption attached to media messages.

    Attributes:
        content: The textual caption, can be None if no caption is provided.
        mentions: Mentions inside the caption, can be a list or dictionary depending on context.
        ext: Additional extension metadata as a dictionary, usually optional.
    """

    content: Optional[str] = Field(None, alias="1")
    """The caption text."""

    mentions: Optional[Union[List, Dict]] = Field(default_factory=dict, alias="2")
    """
    Mentions inside the caption.
    This may include user references or tags.
    Initialized as an empty dict by default.
    """

    ext: Optional[Dict] = Field(default_factory=dict, alias="3")
    """
    Extension metadata related to the caption.
    Used for additional, non-standard information.
    """

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            content: Optional[str] = None,
            mentions: Optional[Union[List, Dict]] = None,
            ext: Optional[Dict] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(content=content, mentions=mentions, ext=ext, **__pydantic_kwargs)


class DocumentMessage(BaleObject):
    """
    Represents a document or file message content.

    Attributes:
        file_id: Unique identifier for the file.
        access_hash: Access hash used for secure file retrieval.
        file_size: Optional size of the file in bytes.
        name: File name; can be a string or a localized dictionary.
        mime_type: MIME type of the file, e.g. "application/pdf".
        ext: Optional additional metadata/extensions as a dictionary.
        caption: Optional caption attached to the document.
    """

    file_id: int = Field(..., alias="1")
    """Unique file identifier."""

    access_hash: int = Field(..., alias="2")
    """Security hash required for accessing the file."""

    file_size: Optional[int] = Field(None, alias="3")
    """File size in bytes, if known."""

    name: Union[Dict, str] = Field(..., alias="4")
    """
    The file name.
    Can be a plain string or a dictionary for localized names.
    """

    mime_type: str = Field(..., alias="5")
    """MIME type describing the file format."""

    ext: Optional[Dict] = Field(None, alias="7")
    """Optional additional metadata or extensions."""

    caption: MessageCaption = Field(..., alias="8")
    """Caption associated with the document message."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            file_id: int,
            access_hash: int,
            file_size: Optional[int] = None,
            name: Union[Dict, str],
            mime_type: str,
            ext: Optional[Dict] = None,
            caption: MessageCaption,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                file_id=file_id,
                access_hash=access_hash,
                file_size=file_size,
                name=name,
                mime_type=mime_type,
                ext=ext,
                caption=caption,
                **__pydantic_kwargs
            )


class MessageContent(BaleObject):
    """
    Container for different types of message content.

    Attributes:
        document: Optional document content if the message includes a file.
        text: Optional text content if the message is a plain text message.
    """

    document: Optional[DocumentMessage] = Field(None, alias="4")
    """Document message content, if present."""

    text: Optional[TextMessage] = Field(None, alias="15")
    """Text message content, if present."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            document: Optional[DocumentMessage] = None,
            text: Optional[TextMessage] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(document=document, text=text, **__pydantic_kwargs)
