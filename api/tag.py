from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from uuid import UUID

from fastapi import Depends
from typing import List

from models.schemas import Tag
from repository.tag import TagRepository

router = APIRouter(
    prefix="/category"
)
repo = TagRepository()

@router.post("/tag/", summary="create a tag")
async def create_tag(req: Tag):
    res = repo.create_tag(name=req.name, task=req.task)
    
    if res == True:
        return JSONResponse(content="tag created", status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content="action incomplete", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
@router.patch("/update/")
async def update_tag_details(id: int, tag: Tag):

    get_tags = repo.get_tag(id=id)
    get_tags = Tag(**get_tags)
    
    udpated_data = tag.model_dump(exclude_unset=True)
    updated_tag = get_tags.model_copy(update=udpated_data)
    
    res = await repo.update_tag(id=id, details=updated_tag)
    
    if res == True:
        return JSONResponse(content="tag updated", status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content="action incomplete", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
@router.delete("/delete/{id}")
async def delete_tag(id: int):
    res = repo.delete_tag(id=id)
    
    if res == True:
        return JSONResponse(content="task deleted", status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content="action incomplete", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
@router.get("/get/{id}", response_model=Tag, summary="Get a single tag")
async def get_tag(id: int):
    res = repo.get_tag(id=id)
    
    if res == 0:
        return JSONResponse(content="action incomplete", status_code=status.HTTP_404_NOT_FOUND)
    
    return res

@router.get("/get/", reposonse_model=List[Tag], summary="List of Tags")
async def get_all_tags():
        return repo.get_tags()