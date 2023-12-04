from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from fastapi import Depends
from typing import List

from models.schemas import Category, CategoryCreate
from repository.category import CategoryRepository

router = APIRouter(
    prefix="/category"
)
repo = CategoryRepository()

@router.post("/create")
async def create_category(req: CategoryCreate):
     
    res = repo.create_category_concise(id=req.id, name=req.name, task_id=req.task_id)
    status = res
   
    if status['success'] == True:
        return JSONResponse(content=status['message'], status_code=201)
    elif status['success'] == False:
        return JSONResponse(content=status['message'], status_code=400)
    
@router.get("/get/{id}")
async def get_category(id: int):
    
    res = repo.get_category_concise(id=id)

    status = res
    print(status)
    
    if status['success'] == True:
        
        data = status['data']
    
        send_out = {}
    
        send_out['id'] = data.id
        send_out['name'] = data.name
        send_out['task'] = data.task_id
        return JSONResponse(content=send_out, status_code=200)
    elif status['success'] == False:
        return JSONResponse(content=status, status_code=404)
    
     
@router.get("/get/", description="Filter or sort to get tasks")
async def sort_filter(
    id: int = Query(None, description="Filter by id"),
    user: str = Query(None, description="Filter by user"),
    sort_by: List[str] = Query(None, description="sort by fields")
):
    query = Category.select()
    
   