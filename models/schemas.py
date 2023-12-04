from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import time, date
from typing import Optional

class Model(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class User(Model):
    id: UUID
    username: str
    email: Optional[str] = None
    password: Optional[str] = None
    
class UserWithoutPasword(Model):
    username: str
    email: Optional[str] = None
    
class UpdateUser(Model):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    

class Task(Model):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    user: Optional[User] = None
    created_at: time
    due_date: date
    
class TaskCreate(Model):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    user_id: UUID
    created_at: time
    due_date: Optional[date] = None
    
class TaskUpdate(Model):
    name: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[UUID] = None
    created_at: Optional[time] = None
    due_date: Optional[date] = None
    
    
# change remind_at to datetime
    
class Reminder(Model):
    id: int
    text: Optional[str] = None
    remind_at: time
    task: Optional[Task] = None
    
class ReminderCreate(BaseModel):
    text: str
    remind_at: time
    task_id: int
    
class ReminderUpdate(BaseModel):
    text: Optional[str] = None
    remind_at: Optional[time] = None
    task_id: Optional[int] = None
    
class Category(Model):
    id: int
    name: Optional[str] = None
    task: Task
    
class CategoryCreate(BaseModel):
    id: int
    name: Optional[str]
    task_id: int
    
class Tag(Model):
    id: int
    name: Optional[str] = None
    task: Task
    
class TaskTag(Model):
    tag: Tag
    task: Task