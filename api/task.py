from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from fastapi import Depends
from typing import List

from models.schemas import Task, TaskCreate, TaskUpdate
from models.peewee_models import Task as TaskDB
from repository.task import TaskRepository

router = APIRouter(
    prefix="/task"
)
repo = TaskRepository()

@router.post("/add/")
async def add_task(req: TaskCreate):
    
    res = repo.insert_task(id=req.id, name=req.name, description=req.description, user=req.user_id, created_at=req.created_at, due_date=req.due_date)
    
    if res == True:
        return JSONResponse(content="task created", status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content="action incomplete", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
@router.patch("/update/")
async def update_task(id: int, task: TaskUpdate):
    
    updated_data = task.model_dump(exclude_unset=True)
    
    result = repo.update_task(id=id, details=updated_data)
         
    if result == True:
        return JSONResponse(content="task modified", status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content="action incomplete", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
@router.delete("/delete/{id}")
async def delete_task(id: int):
    res = repo.delete_task(id=id)
    
    if res == True:
        return JSONResponse(content="task deleted", status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content="action incomplete", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
@router.get("/get/{id}", response_model=Task, summary="Get a single task", response_model_exclude={'user': {"password", "id", "email"}})
async def get_task(id: int):
    res = repo.get_task(id=id)
    
    if res == 0:
        return JSONResponse(content="action incomplete", status_code=status.HTTP_404_NOT_FOUND)
    
    return res

@router.get("/all/", response_model=List[Task], summary="List of Tasks")
async def get_all_tasks():
        print("works for now")
        return repo.get_all_tasks()
    
    
@router.get("/get/", summary="Filter or sort task records")
async def get_tasks(
    id: int = Query(None, description="Filter by Id"),
    name: str = Query(None, description="Filter by name"),
    sort_by: List[str] = Query([], description="Sort by user record fields")
):
    
    query = TaskDB.select()
    
    if id:
        query = query.where(TaskDB.id == id)
    elif name:
        query = query.where(TaskDB.name == name)
        
    for field in reversed(sort_by):
        reverse_order = field.startswith("-")
        field = field.lstrip("-")
        query = query.order_by(getattr(TaskDB, field).desc() if reverse_order else getattr(TaskDB, field))
    
    
    # TODO Add 404s
    # Execute the query
    result_tasks = [task for task in query.dicts()]

    return result_tasks if result_tasks != [] else {"message": "record doesn't exist",  "records": result_tasks}