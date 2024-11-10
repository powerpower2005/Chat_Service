from typing import Optional
from pymongo import MongoClient
from .config import settings

class Database:
    client: Optional[MongoClient] = None
    
    def connect_to_database(self):
        self.client = MongoClient(settings.mongodb_url)
        
    def close_database_connection(self):
        if self.client is not None:
            self.client.close()
            
    def get_db(self):
        if self.client is None:
            self.connect_to_database()
        return self.client[settings.db_name]

# 데이터베이스 인스턴스 생성
db = Database()