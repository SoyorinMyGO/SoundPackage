from datetime import datetime
from pydantic import BaseModel


class Voice(BaseModel):
    id: int
    name: str
    length: int
    used_times: int
    created_at: datetime
    updated_at: datetime