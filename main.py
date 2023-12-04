import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from contextlib import asynccontextmanager

from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from db_config.peewee_connect import db

from typing import Union
from models.peewee_models import User, Reminder, Task, Tag, Category
from api import reminder, task, user, category
from logger import logger

from fastapi.responses import JSONResponse

models = {
        'User': User,
        'Reminder': Reminder,
        'Task': Task,
        'Tag': Tag,
        'Category': Category
    }

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    db.connect()
    
    for _, model_class in models.items():
        # db.drop_tables(models=[model_class])
        if not model_class.table_exists():
            db.create_tables([model_class])
            logger.info("creating " + model_class.__name__)
        else:
            logger.info(model_class.__name__ + " DB tables have been created")
    yield 
    
    db.close()

app = FastAPI(lifespan=lifespan)
security = HTTPBasic()

@app.get("/items/")
async def read_items(q: Union[str, None] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/")
async def index(credentials: HTTPBasicCredentials = Depends(security)):
    
    curr_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"yums"
    
    is_correct_username = secrets.compare_digest(
        curr_username_bytes, correct_username_bytes
    )
    
    curr_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    
    is_correct_password = secrets.compare_digest(
        curr_password_bytes, correct_password_bytes
    )
    
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    # return credentials.username    

    return JSONResponse(content="Welcome to Task Management System", status_code=200)

app.include_router(user.router)
app.include_router(reminder.router)
app.include_router(task.router)
app.include_router(category.router)