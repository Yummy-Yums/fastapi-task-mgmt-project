from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from fastapi import Depends
from typing import List

from models.schemas import Reminder, ReminderCreate, ReminderUpdate
from models.peewee_models import Reminder as ReminderDB

from repository.reminder import ReminderRepository

router = APIRouter(
    prefix="/reminder"
)
repo = ReminderRepository()

@router.post("/add/")
async def add_reminder(req: ReminderCreate):

    res = repo.create_reminder(text=req.text,remind_at=req.remind_at,task_id=req.task_id)
  
    if res == True:
        return JSONResponse(content="reminder has been created", status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content="reminder not created", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
@router.patch("/update/")
async def update_reminder(id: int, reminder: ReminderUpdate):
    # get the resource
    
    update_data = reminder.model_dump(exclude_unset=True)
    
    result =  repo.update_reminder(id=id, details=update_data)
    
    if result == True:
        return JSONResponse(content="reminder modified", status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content="reminder not modified", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
@router.delete("/delete/{id}")
async def delete_reminder(id: int):
    res = repo.delete_reminder(id=id)
    
    if res == True:
        return JSONResponse(content="reminder has been deleted", status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content="action incomplete", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    

@router.get("/get/{id}", response_model=Reminder, summary="Get single reminder")
async def get_reminder(id: int):
    res = repo.get_reminder(id=id)
    
    if res == 0:
        return JSONResponse(content="reminder not found", status_code=status.HTTP_404_NOT_FOUND)
    
    return res

@router.get("/all/", response_model=List[Reminder], summary="List of reminders")
async def get_all_reminders():
   return repo.get_reminders()


@router.get("/get/", summary="Filter or sort user records")
async def get_reminders(
    id: int = Query(None, description="Filter by Id"),
    text: str = Query(None, description="Filter by text"),
    sort_by: List[str] = Query([], description="Sort by user record fields")
):
    
    query = ReminderDB.select()
    
    if id:
        query = query.where(ReminderDB.id == id)
    elif text:
        query = query.where(ReminderDB.text.contains(text))
        
    for field in reversed(sort_by):
        reverse_order = field.startswith("-")
        field = field.lstrip("-")
        query = query.order_by(getattr(ReminderDB, field).desc() if reverse_order else getattr(ReminderDB, field))
        
    # Execute the query
    result_reminders = [reminder for reminder in query.dicts()]

    return result_reminders if result_reminders != [] else {"message": "record doesn't exist",  "records": result_reminders}
