from fastapi import WebSocket, APIRouter, Query
from fastapi.websockets import WebSocketDisconnect
import json
from datetime import datetime
from ..services.user_service import UserService
from ..services.chat_service import ChatService
from ..models.chat import ChatMessageCreate
from ..utils.auth import decode_token
from ..websocket.manager import ConnectionManager
router = APIRouter()

user_service = UserService()
chat_service = ChatService()
manager = ConnectionManager()
@router.websocket("/ws/chat/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    room_id: str,
    token: str = Query(...)
):
    """WebSocket 엔드포인트"""
    try:
        email = decode_token(token)
        user = user_service.get_user_by_email(email)
        if not user:
            await websocket.close(code=4001)
            return

        await manager.connect(websocket, room_id)
        
        # 이전 메시지 히스토리 전송
        messages = await chat_service.get_room_messages(room_id)
        for message in messages:
            await websocket.send_json({
                "id": str(message.id),
                "content": message.content,
                "sender_id": message.sender_id,
                "username": user_service.get_user(message.sender_id).username,
                "created_at": str(message.created_at),
                "type": "history"  # 히스토리 메시지임을 표시
            })
        
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            chat_message = ChatMessageCreate(
                content=message_data["content"],
                room_id=room_id,
                sender_id=str(user.id)
            )
            saved_message = chat_service.save_message(chat_message)
            
            await manager.broadcast(
                json.dumps({
                    "id": str(saved_message.id),
                    "content": saved_message.content,
                    "sender_id": saved_message.sender_id,
                    "username": user.username,
                    "created_at": str(saved_message.created_at),
                    "type": "message"  # 실시간 메시지임을 표시
                }),
                room_id
            )
            
    except WebSocketDisconnect:
        await manager.disconnect(websocket, room_id)
        await manager.broadcast(
            json.dumps({
                "type": "system",
                "content": f"{user.username}님이 채팅방을 나갔습니다.",
                "timestamp": str(datetime.utcnow())
            }),
            room_id
        ) 