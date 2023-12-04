import bcrypt
# from models.peewee_models import User, Reminder, Task, Tag, Category
from typing import Any, Dict
import peewee
import re

def create_table_name(model_class):
    model_name = model_class.__name__
    return model_name.lower() + ' table'

def hash_password(input_password: str):
    byte_passwd = input_password.encode('utf-8')
    
    hashed_password = bcrypt.hashpw(byte_passwd, bcrypt.gensalt())
    hashed_password = hashed_password.decode('utf-8')
    
    return hashed_password

def format_uuid(uuid_str):
    if len(uuid_str) == 32 and uuid_str.isalnum():
        formatted_uuid = f"{uuid_str[:8]}-{uuid_str[8:12]}-{uuid_str[12:16]}-{uuid_str[16:20]}-{uuid_str[20:]}"
        return formatted_uuid
    else:
        raise ValueError("Invalid UUID string format")

# TODO Exception Handlers


def validate_email(email):
    emailRegex = re.compile(r'''(
        [a-zA-Z0-9._%+-]+  #username
        @                  # @ symbol
        [a-zA-A0-9.-]+     # domain name
        (\.[a-zA-Z]{2,4})  # dot-something                 
    )''', re.VERBOSE)
    
    bool(emailRegex.match(email))

# TODO function to abstract response ?

# TODO common function for repo queries


def safe_query(query) -> Any:
    try:
        if isinstance(query, peewee.ModelInsert):
            query.execute()  # Insert operation
            return {"success": True, "message": "Insert successful"}
        elif isinstance(query, peewee.ModelUpdate):
            rows_updated = query.execute()  # Update operation
            return {"success": True, "message": f"Updated {rows_updated} rows"}
        elif isinstance(query, peewee.ModelDelete):
            rows_deleted = query.execute()  # Delete operation
            return {"success": True, "message": f"Deleted {rows_deleted} rows"}
        else:
            try:
                result = query.get()  # Select operation
                return {"success": True, "data": result}
            except peewee.DoesNotExist as e:
                
                return {"success": False, "message": "No matching records found"}
    except peewee.PeeweeException:
        return {"success": False, "message": "Query failed"}

# # Example usage:
# user = User(username="john")
# result = safe_query(user.save(), User)  # Insert
# print(result)

# user.username = "new_john"
# query = User.update(username="new_john").where(User.username == "john")
# result = safe_query(query, User)  # Update
# print(result)

# query = User.delete().where(User.username == "new_john")
# result = safe_query(query, User)  # Delete
# print(result)

# query = User.select().where(User.username == "new_john")
# result = safe_query(query, User)  # Select
# print(result)
