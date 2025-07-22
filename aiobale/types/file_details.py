from typing import Optional
from pydantic import BaseModel


class FileDetails(BaseModel):
    name: str
    size: int
    mime_type: str
    file_id: int
    access_hash: int
