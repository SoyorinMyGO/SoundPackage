from datetime import datetime
from pydantic import BaseModel


class Voice(BaseModel):
    id: int | None = None
    remote_id: int | None = None
    name: str
    length: int
    used_times: int = 0
    hash_content: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()