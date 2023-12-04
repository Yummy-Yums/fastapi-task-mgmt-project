from db_config.peewee_connect import db
from peewee import *
from util import create_table_name
import uuid

# Add lazy load to all models
class BaseModel(Model):
    class Meta:
        database = db
        table_name = create_table_name
         
class UUIDField(Field):
    field_type = 'uuid'
    
    def db_value(self, value):
        return value.hex  # convert UUID to hex string.
    
    def python_value(self, value):
        return uuid.UUID(value) # convert hex string to UUID
        
class User(BaseModel):
    id = UUIDField(null=False, primary_key=True)
    username = CharField(unique=True, null=True)
    email = CharField(max_length=80, unique=True)
    password = CharField(null=True)
    # user must have a list of tasks
         
class Task(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(unique=True, max_length=60)
    description = TextField()
    user = ForeignKeyField(User, backref='tasks', unique=True, on_delete='SET NULL', on_update='CASCADE')
    created_at = TimeField()
    due_date = DateField()
    
class Tag(BaseModel):
    id = AutoField(primary_key=True, null=True)
    name = CharField(max_length=60)
    task = ForeignKeyField(Task, backref='tags', on_delete='SET NULL', on_update='CASCADE')
    
class Task_Tag(BaseModel):
     id = AutoField(primary_key=True)
     tag = ForeignKeyField(Tag, backref='task_tag')
     task = ForeignKeyField(Task, backref='task_tag')
    
class Reminder(BaseModel):
    id = AutoField(primary_key=True)
    text = TextField()
    remind_at = TimeField()
    task = ForeignKeyField(Task, backref='reminders', on_delete='SET NULL', on_update='CASCADE')
    
class Category(BaseModel):
    id = AutoField(primary_key=True, null=True)
    name = CharField(max_length=60, null=True)
    task =  ForeignKeyField(Task, backref='categories', on_delete='SET NULL', on_update='CASCADE', null=True)