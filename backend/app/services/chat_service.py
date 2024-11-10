from typing import List, Optional
from bson.objectid import ObjectId
from datetime import datetime
from ..database import db
from ..models.chat import ChatRoom, ChatMessageDB, ChatMessageCreate
import logging

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.db = db.get_db()
        self.chat_rooms = self.db["chat_rooms"]
        self.chat_messages = self.db["chat_messages"]

    def create_room(self, room: ChatRoom) -> ChatRoom:
        """새로운 채팅방 생성"""
        room_dict = room.dict(exclude={'id'})
        result = self.chat_rooms.insert_one(room_dict)
        room.id = str(result.inserted_id)
        return room

    def get_room(self, room_id: str) -> Optional[ChatRoom]:
        """채팅방 정보 조회"""
        room_data = self.chat_rooms.find_one({"_id": ObjectId(room_id)})
        if room_data:
            room_data['id'] = str(room_data.pop('_id'))
            return ChatRoom(**room_data)
        return None

    def add_participant(self, room_id: str, user_id: str) -> bool:
        """채팅방에 참가자 추가"""
        result = self.chat_rooms.update_one(
            {"_id": ObjectId(room_id)},
            {"$addToSet": {"participants": user_id}}
        )
        return result.modified_count > 0

    def save_message(self, message: ChatMessageCreate) -> ChatMessageDB:
        """채팅 메시지 저장"""
        message_data = message.dict()
        message_data["id"] = str(ObjectId())
        message_db = ChatMessageDB(**message_data)
        message_dict = message_db.dict(exclude={'id'})
        result = self.chat_messages.insert_one(message_dict)
        message_db.id = str(result.inserted_id)
        return message_db

    async def get_room_messages(self, room_id: str, limit: int = 100) -> List[ChatMessageDB]:
        """채팅방의 메시지 이력 조회"""
        messages = []
        cursor = self.chat_messages.find(
            {"room_id": room_id, "is_deleted": False}
        ).sort("created_at", 1).limit(limit)  # 시간순 정렬, 최근 100개
        
        for message in cursor:
            message['id'] = str(message.pop('_id'))
            messages.append(ChatMessageDB(**message))
        
        return messages

    def remove_participant(self, room_id: str, user_id: str) -> bool:
        """채팅방에서 참가자 제거"""
        result = self.chat_rooms.update_one(
            {"_id": ObjectId(room_id)},
            {"$pull": {"participants": user_id}}
        )
        return result.modified_count > 0

    def get_rooms(self) -> List[ChatRoom]:
        """모든 채팅방 목록 조회"""
        try:
            rooms = []
            cursor = self.chat_rooms.find()
            
            if cursor is None:
                logger.warning("No chat rooms found")
                return []
                
            for room in cursor:
                try:
                    room['id'] = str(room.pop('_id'))
                    rooms.append(ChatRoom(**room))
                except Exception as e:
                    logger.error(f"Error processing room data: {str(e)}")
                    continue
                    
            logger.info(f"Retrieved {len(rooms)} chat rooms")
            return rooms
        except Exception as e:
            logger.error(f"Error getting chat rooms: {str(e)}", exc_info=True)
            raise