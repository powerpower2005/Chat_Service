from typing import Optional, List
from bson import ObjectId
from ..models.user import UserInDB, UserCreate, UserResponse
import bcrypt
from ..database import db
from datetime import datetime

def hash_password(password: str) -> str:
    """Hash the password"""
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
        # Hash the password
        hashed_password = hash_password(user_data.password)
        
        # Prepare user data
        user_dict = {
            "email": user_data.email,
            "username": user_data.username,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow(),
            "is_active": True
        }
        
        # Save to DB
        result = self.collection.insert_one(user_dict)
        
        # Return saved user information
        user_dict["id"] = str(result.inserted_id)
        return UserResponse(**user_dict)

    def search_users(self, query: str) -> List[UserResponse]:
        """
        Search users by email.
        Case-insensitive and partial match search is supported.
        """
        # Use MongoDB regex search
        users = self.collection.find({
            "email": {"$regex": query, "$options": "i"}  # i option: case-insensitive
        }).limit(10)  # Limit search results
        
        return [UserResponse(**user) for user in users]

    def get_user(self, user_id: str) -> Optional[UserInDB]:
        """Get user information by user ID"""
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user['id'] = str(user.pop('_id'))
            return UserInDB(**user)
        return None