from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class AbstractEntity(BaseModel):
    id: Optional[int]


class TodoEntry(AbstractEntity):
    summary: str
    detail: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    tags: List[str] = list()
