from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..models.chat import ChatRoom, ChatMessageDB
from ..services.chat_service import ChatService
from ..utils.auth import oauth2_scheme, decode_token, get_current_user
from ..models.user import User
from ..services.user_service import UserService
import logging

router = APIRouter()
chat_service = ChatService()
user_service = UserService()
logger = logging.getLogger(__name__)

@router.post("/rooms", response_model=ChatRoom)
def create_chat_room(
    room: ChatRoom,
    token: str = Depends(oauth2_scheme)
):
    """Create a new chat room"""
    try:
        # Extract email from token
        email = decode_token(token)
        logger.info(f"Decoded email from token: {email}")
        
        # Get user information by email
        user = user_service.get_user_by_email(email)
        logger.info(f"Found user: {user}")
        
        if not user:
            logger.error(f"User not found for email: {email}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Set chat room creator information
        room.created_by = user.username
        room.participants = [str(user.id)]
        
        logger.info(f"Creating chat room with name: {room.name} by user: {room.created_by}")
        created_room = chat_service.create_room(room)
        logger.info(f"Successfully created chat room with id: {created_room.id}")
        
        return created_room
    except Exception as e:
        logger.error(f"Failed to create chat room: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create chat room: {str(e)}"
        )

@router.get("/rooms/{room_id}")
async def get_room(room_id: str, current_user: User = Depends(get_current_user)):
    """채팅방 정보 조회"""
    room = chat_service.get_room(room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat room not found"
        )
    messages = await chat_service.get_room_messages(room_id)
    return {
        "name": room.name,
        "messages": messages,
        "currentUserId": str(current_user.id)
    }

@router.post("/rooms/{room_id}/join")
async def join_chat_room(
    room_id: str,
    token: str = Depends(oauth2_scheme)
):
    """채팅방 참여"""
    user = user_service.get_user_by_email(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    success = chat_service.add_participant(room_id, str(user.id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to join chat room"
        )
    return {"message": "Successfully joined chat room"}

@router.get("/rooms/{room_id}/messages", response_model=List[ChatMessageDB])
async def get_chat_messages(
    room_id: str,
    token: str = Depends(oauth2_scheme)
):
    """채팅방 메시지 이력 조회"""
    messages = await chat_service.get_room_messages(room_id)
    return messages

@router.post("/rooms/{room_id}/leave")
async def leave_chat_room(
    room_id: str,
    token: str = Depends(oauth2_scheme)
):
    """채팅방 나가기"""
    user = await user_service.get_user_by_email(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    success = await chat_service.remove_participant(room_id, str(user.id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to leave chat room"
        )
    return {"message": "Successfully left chat room"}

@router.get("/rooms", response_model=List[ChatRoom])
def get_chat_rooms(token: str = Depends(oauth2_scheme)):
    """모든 채팅방 목록 조회"""
    try:
        rooms = chat_service.get_rooms()
        logger.info(f"Successfully retrieved chat rooms")
        return rooms
    except Exception as e:
        logger.error(f"Failed to get chat rooms: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get chat rooms: {str(e)}"
        )

@router.post("/{room_id}/invite/{user_id}")
async def invite_to_chat(
    room_id: str,
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    # 방이 존재하는지 확인
    room = chat_service.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="채팅방을 찾을 수 없습니다")
    
    # 초대하는 사람이 해당 방의 참가자인지 확인
    if current_user.id not in room.participants:
        raise HTTPException(status_code=403, detail="초대 권한이 없습니다")
    
    # 사용자가 존재하는지 확인
    invited_user = user_service.get_user(user_id)
    if not invited_user:
        raise HTTPException(status_code=404, detail="초대할 사용자를 찾을 수 없습니다")
    
    # 이미 참가자인지 확인
    if user_id in room.participants:
        raise HTTPException(status_code=400, detail="이미 채팅방에 참가중인 사용자입니다")
    
    # 참가자 추가
    success = chat_service.add_participant(room_id, user_id)
    if success:
        return {"message": "사용자가 성공적으로 초대되었습니다"}
    else:
        raise HTTPException(status_code=500, detail="초대 처리 중 오류가 발생했습니다")