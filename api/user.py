from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from uuid import UUID

from fastapi import Depends
from typing import List

from models.schemas import User, UserWithoutPasword, UpdateUser
from models.peewee_models import User as UserDB
from repository.user import UserRepository

router = APIRouter(
    prefix="/user"
)
repo = UserRepository()

@router.post("/add/")
async def add_user(req: User):
    #TODO decide on validator
        
    res = repo.create_user(id=req.id, username=req.username, email=req.email, password=req.password)
    
    if res == True:
        return JSONResponse(content="user created", status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content="action incomplete", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
@router.patch("/update/")
async def update_user_details(id: UUID, user: UpdateUser):
    
    updated_data = user.model_dump(exclude_unset=True)
    
    result =  repo.update_details(id=id, details=updated_data)
    
    if result == True:
        return JSONResponse(content="user updated", status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content="action incomplete", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
@router.delete("/delete/{id}")
async def delete_user(id: UUID):
    
    res = repo.delete_user(id=id)
    
    # create a redirect
    
    if res == True:
        return JSONResponse(content="user_details deleted", status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content="action incomplete", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    

@router.get("/{id}", response_model=User, summary="Get a single user", response_model_exclude={"password"})
async def get_single_user(id: UUID):
    res = repo.get_user(id=id)
    
    if res == None:
        return JSONResponse(content="action incomplete", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    return res


@router.get("/all/", response_model=List[UserWithoutPasword], summary="Get all  users", response_model_exclude={"username", "password"})
async def get_all_user():
    
    all_users = repo.get_all_users()
    
    users = []
    
    for user in all_users:
        
        users.append({
            "username": user.username,
            "email": user.email
        })

    return users

@router.get("/get/", summary="Filter or sort user records")
async def get_users(
    id: UUID = Query(None, description="Filter by Id"),
    name: str = Query(None, description="Filter by name"),
    sort_by: List[str] = Query([], description="Sort by user record fields")
):
    
    query = UserDB.select()
    
    if id:
   
        query = query.where(UserDB.id == id)
    elif name:
        query = query.where(UserDB.username == name)
        
    for field in reversed(sort_by):
        reverse_order = field.startswith("-")
        field = field.lstrip("-")
        query = query.order_by(getattr(UserDB, field).desc() if reverse_order else getattr(UserDB, field))
        
    # Execute the query
    result_users = [user for user in query.dicts()]

    return result_users if result_users != [] else {"message": "record doesn't exist",  "records": result_users}