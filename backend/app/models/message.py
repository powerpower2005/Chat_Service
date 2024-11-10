from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ChatMessageCreate(BaseModel):
    content: str
    room_id: str
    sender_id: str

class ChatMessageDB(ChatMessageCreate):
    id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_deleted: bool = False
    is_system_message: bool = False 