import os
import io
import mimetypes
from pathlib import Path
from typing import Union, Optional, NamedTuple

from .file_details import FileDetails
from ..utils import guess_mime_type


class FileData(NamedTuple):
    name: str
    size: int
    mime_type: str


class FileInput:
    def __init__(
        self,
        file: Union[str, Path, bytes],
        *,
        name: Optional[str] = None,
        size: Optional[int] = None,
        mime_type: Optional[str] = None,
    ):
        if isinstance(file, (str, Path)):
            self._type = "path"
            self._path = Path(file)
        elif isinstance(file, bytes):
            self._type = "bytes"
            self._bytes = file
        else:
            raise TypeError("Unsupported file type")

        self.info = self._info(name=name, size=size, mime_type=mime_type)

    async def read(self, chunk_size: int = 4096):
        if self._type == "path":
            import aiofiles

            async with aiofiles.open(self._path, "rb") as f:
                while True:
                    chunk = await f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
        elif self._type == "bytes":
            buf = io.BytesIO(self._bytes)
            while True:
                chunk = buf.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    def _info(
        self, name: Optional[str], size: Optional[str], mime_type: Optional[str]
    ) -> FileData:
        if self._type == "path":
            path = self._path
            name = name or path.name
            size = size or os.path.getsize(path)
            mime_type = (
                mime_type
                or mimetypes.guess_type(path.name)[0]
                or "application/octet-stream"
            )
        elif self._type == "bytes":
            b = self._bytes
            size = size or len(b)
            mime_type = mime_type or guess_mime_type(b[:32])
            if not name:
                ext = mime_type.split("/")[-1]
                name = f"upload.{ext if ext.isalnum() else 'dat'}"

        return FileData(name=name, size=size, mime_type=mime_type)
    
    async def get_content(self) -> bytes:
        chunks = []
        async for chunk in self.read():
            chunks.append(chunk)
        return b''.join(chunks)
