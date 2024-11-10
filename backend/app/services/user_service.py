from typing import Optional, List
from bson import ObjectId
from ..models.user import UserInDB, UserCreate, UserResponse
import bcrypt
from ..database import db
from datetime import datetime

def hash_password(password: str) -> str:
    """비밀번호를 해시화"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

class UserService:
    def __init__(self):
        self.db = db.get_db()
        self.collection = self.db["users"]

    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        user = self.collection.find_one({"email": email})
        if user:
            user['id'] = str(user.pop('_id'))
            return UserInDB(**user)
        return None

    def create_user(self, user_data: UserCreate) -> UserResponse:
        # 비밀번호 해시화
        hashed_password = hash_password(user_data.password)
        
        # 사용자 데이터 준비
        user_dict = {
            "email": user_data.email,
            "username": user_data.username,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow(),
            "is_active": True
        }
        
        # DB에 저장
        result = self.collection.insert_one(user_dict)
        
        # 저장된 사용자 정보 반환
        user_dict["id"] = str(result.inserted_id)
        return UserResponse(**user_dict)

    def search_users(self, query: str) -> List[UserResponse]:
        """
        이메일로 사용자를 검색합니다.
        대소문자를 구분하지 않고 부분 일치도 검색됩니다.
        """
        # MongoDB regex 검색 사용
        users = self.collection.find({
            "email": {"$regex": query, "$options": "i"}  # i 옵션: 대소문자 구분 없음
        }).limit(10)  # 검색 결과 제한
        
        return [UserResponse(**user) for user in users]

    def get_user(self, user_id: str) -> Optional[UserInDB]:
        """사용자 ID로 사용자 정보를 조회"""
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user['id'] = str(user.pop('_id'))
            return UserInDB(**user)
        return None