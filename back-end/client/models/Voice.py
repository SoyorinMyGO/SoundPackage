from datetime import datetime
from pydantic import BaseModel


class Voice(BaseModel):
    id: int | None = None
    remote_id: int | None
    name: str
    length: int
    used_times: int
    hash_content: str
    created_at: datetime
    updated_at: datetime