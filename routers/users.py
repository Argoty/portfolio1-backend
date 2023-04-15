from fastapi import APIRouter, HTTPException
from db.models.user import User
from db.schemas.user import users_schema
from db.client import db_client
from bson import ObjectId
from searcher import search_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"message": "No encontrado"}})


@router.get("/", response_model=list[User])
async def get_users():
    return users_schema(db_client.users.find())

@router.get("/{id}", response_model=User)
async def get_user(id: str):
    try:
        user = search_user("_id", ObjectId(id))
    except:
        raise HTTPException(status_code=404, detail="User doesn't exist")

    if not type(user) == User:
        raise HTTPException(status_code=404, detail="User doesn't exist")

    return user



@router.post("/", status_code=201, response_model=User)
async def create_user(user: User):
    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    return search_user("_id", id)


@router.put("/", response_model=User)
async def update_user(user: User):
    try:
        if not type(search_user("_id", ObjectId(user.id))) == User:
            raise HTTPException(
                status_code=404, detail="User doesn't exist")
    except:
        raise HTTPException(status_code=404, detail="User doesn't exist")

    user_dict = dict(user)
    del user_dict["id"]

    db_client.users.find_one_and_replace(
        {"_id": ObjectId(user.id)}, user_dict)

    return search_user("_id", ObjectId(user.id))


@router.delete("/{id}", status_code=204)
async def delete_user(id: str):
    try: 
        user_eliminated = db_client.users.find_one_and_delete({"_id": ObjectId(id)}) 
    except:
        raise HTTPException(status_code=404, detail="User doesn't exist")

    if not user_eliminated:
        raise HTTPException(status_code=404, detail="User doesn't exist")