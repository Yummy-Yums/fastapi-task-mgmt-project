from models.peewee_models import Reminder, User, Task
from datetime import time, date
from typing import Dict, Any

from fastapi.encoders import jsonable_encoder

class ReminderRepository:
    
    def create_reminder(self, text:str, remind_at:time, task_id:int) -> bool:
        try:
            
            model = Reminder(text=text,remind_at=remind_at,task=task_id)
            model.save()
            # Reminder.create(text=text, remind_at=remind_at, task=jsonable_encoder(task))

        except Exception as e:
            print(e)
            return False
        return True
    
    def update_reminder(self, id: int, details: Dict[str, Any]) -> bool:
        try:
            serialized_data = jsonable_encoder(details)
            query = Reminder.update(**serialized_data).where(Reminder.id == id)
            query.execute()
        except Exception as e:
            print(e)
            return False
        return True
    
    def delete_reminder(self, id: int) -> bool:
        try:
            Reminder.delete_by_id(id)
        except Exception as e:
            print(e)
            return False
        return True
    
    def get_reminder(self, id: int):
        try:
            q = Reminder.get_by_id(id)
            
        except Exception as e:
            print(e)
            return 0
        
        return q
    
    def get_reminders(self):
        return list(Reminder.select())
    
    # exception handlers maybe?