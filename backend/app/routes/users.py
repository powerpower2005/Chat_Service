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
    Search users by email.
    q: search query (email)
    """
    users = user_service.search_users(q)
    # Exclude current user from search results
    users = [user for user in users if user.id != current_user.id]
    return users 