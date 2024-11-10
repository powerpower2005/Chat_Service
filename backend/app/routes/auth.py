from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from datetime import timedelta
from ..models.user import UserCreate, User, UserResponse
from ..services.user_service import UserService
from ..utils.auth import create_access_token, verify_password
from ..config import settings
from ..database import db
import logging

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
user_service = UserService()
logger = logging.getLogger(__name__)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    try:
        # Check if email already exists
        if user_service.get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        user = user_service.create_user(user_data)
        return user
        
    except Exception as e:
        print(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not register user"
        )

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = user_service.get_user_by_email(form_data.username)
        if not user or not verify_password(form_data.password, user.hashed_password):
            logger.warning(f"Login failed for user: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Login error for user {form_data.username}: {str(e)}", exc_info=True)
        raise