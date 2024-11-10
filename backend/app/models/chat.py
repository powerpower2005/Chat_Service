from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.database import db

class ChatRoom(BaseModel):
    id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=100)
    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    participants: List[str] = Field(default_factory=list)

class ChatMessageCreate(BaseModel):
    content: str
    room_id: str
    sender_id: str

class ChatMessageDB(ChatMessageCreate):
    id: Optional[str]
    created_at: datetime = datetime.utcnow()
    is_deleted: bool = False 

class MessageValidator:
    @staticmethod
    def validate_message(message: str) -> bool:
        if not message or len(message.strip()) == 0:
            return False
        if len(message) > 1000:  # 최대 메시지 길이 제한
            return False
        return True 

    async def get_room_messages(self, room_id: str, limit: int = 50) -> List[ChatMessageDB]:
        messages = []
        cursor = db.get_db().chat_messages.find(
            {"room_id": room_id, "is_deleted": False}
        ).sort("created_at", -1).limit(limit)
        
        async for message in cursor:
            message['id'] = str(message.pop('_id'))
            messages.append(ChatMessageDB(**message))
        
        return messages[::-1]  # 시간순 정렬 