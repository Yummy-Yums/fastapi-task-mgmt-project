from models.peewee_models import User
from typing import Dict, Any
from util import hash_password
from uuid import UUID

class UserRepository:
    def create_user(self, id: UUID, username: str, email: str, password: str) -> bool:
        
        #check whether password is empty
        hashed_password = hash_password(password)
      
        try:
            User.create(id=id, username=username, email=email, password=hashed_password)
        except Exception as e:
            print(e)
            return False
        return True
    
    def get_user(self, id: UUID):
        return User.get_by_id(id)
    
    def get_all_users(self):
        return list(User.select())
        
    def update_details(self, id: int, details: Dict[str, Any]) -> bool:
        try:
            query = User.update(**details).where(User.id == id)
            query.execute()
        except Exception as e:
            print(e)
            return False
        return True
    
    def delete_user(self, id: UUID):
        try:
            User.delete_by_id(id)
        except Exception as e:
            print(e)
            return False
        return True 
    
    def delete_all_users(self):
        pass        