from models.peewee_models import *
from datetime import time, date
from typing import Dict, Any

# TODO check the Model class method to raise exceptions

class TaskRepository:
    
    def insert_task(self, id: int, name: str, description: str, user: User, created_at: time, due_date: date):
        
        try:
            Task.create(task_id=id, name=name, description=description, user=user, created_at=created_at, due_date=due_date)    
        except Exception as e:
            print(e)
            return False
        return True
    
    def update_task(self, id: int, details: Dict[str, Any]) -> bool:
        try:
            query = Task.update(**details).where(Task.id == id)   
            query.execute()
        except Exception as e:
            print(e)
            return False
        return True
    
    def delete_task(self, id: int):
        try:
            # check if the task exists , if not throw error
            Task.delete_by_id(id)
        except: 
            return False 
        return True
    
    def get_task(self, id: int):
        try:
            q = Task.get_by_id(id)
        except: 
            return 0 
        return q
    
    def get_all_tasks(self):
        return list(Task.select())
