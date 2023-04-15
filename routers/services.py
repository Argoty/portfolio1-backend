from fastapi import APIRouter, HTTPException
from db.models.user import Service, User
from db.client import db_client
from bson import ObjectId
from searcher import search_services, search_user, search_service

router = APIRouter(
    prefix="/services",
    tags=["services"],
    responses={404: {"message": "No encontrado"}})




@router.get("/{id_user}", response_model=list[Service])
async def get_user_services(id_user):
    user_services = search_services(id_user)

    if len(user_services) <= 0:
        raise HTTPException(
            status_code=404, detail="The user doesn't exist or there aren't services")

    return user_services

@router.post("/", response_model=Service, status_code=201)
async def create_service(service: Service):
    try:
        if not type(search_user("_id", ObjectId(service.id_user))) == User:
            raise HTTPException(status_code=404, detail="User not found")
    except:
        raise HTTPException(status_code=404, detail="User not found")

    service_dict = dict(service)

    del service_dict["id"]

    id = db_client.services.insert_one(service_dict).inserted_id
    return search_service("_id", id)



@router.put("/", response_model=Service)
async def update_service(service: Service):
    try:
        if not type(search_service("_id", ObjectId(service.id))) == Service:
            raise HTTPException(status_code=404, detail="service not found")
    except:
        raise HTTPException(status_code=404, detail="service not found")
    
    try:
        if not type(search_user("_id", ObjectId(service.id_user))) == User:
            raise HTTPException(status_code=404, detail="User not found")
    except:
        raise HTTPException(status_code=404, detail="User not found")


    service_dict = dict(service)
    del service_dict["id"]

    db_client.services.find_one_and_replace({ "_id": ObjectId(service.id)}, service_dict)  

    return search_service("_id", ObjectId(service.id))


@router.delete("/{id}", status_code=204)
async def delete_service(id: str):
    try: 
        service_eliminated = db_client.services.find_one_and_delete({"_id": ObjectId(id)}) 
    except:
        raise HTTPException(status_code=404, detail="service not found")

    if not service_eliminated:
        raise HTTPException(status_code=404, detail="service not found")