from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
from ..models.user import User, UserResponse
from ..services.user_service import UserService
from ..utils.auth import get_current_user



router = APIRouter()
user_service = UserService()

@router.get("/search", response_model=List[UserResponse])
async def search_users(
    q: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_user)
):
    """
    이메일로 사용자를 검색합니다.
    q: 검색어 (이메일)
    """
    users = user_service.search_users(q)
    # 현재 사용자는 검색 결과에서 제외
    users = [user for user in users if user.id != current_user.id]
    return users 