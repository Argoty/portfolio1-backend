from fastapi import APIRouter, HTTPException
from db.models.user import Project, User
from db.client import db_client
from bson import ObjectId
from searcher import search_project, search_projects, search_user

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={404: {"message": "No encontrado"}})


@router.get("/{id}", response_model=Project)
async def get_project(id: str):
    try:
        project = search_project("_id", ObjectId(id))
    except:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if not type(project) == Project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project


@router.get("/user/{id_user}", response_model=list[Project])
async def get_user_projects(id_user):
    user_projects = search_projects(id_user)

    if len(user_projects) <= 0:
        raise HTTPException(
            status_code=404, detail="The user doesn't exist or there aren't projects")

    return user_projects

@router.post("/", response_model=Project, status_code=201)
async def create_project(project: Project):
    try:
        if not type(search_user("_id", ObjectId(project.id_user))) == User:
            raise HTTPException(status_code=404, detail="User not found")
    except:
        raise HTTPException(status_code=404, detail="User not found")

    if type(search_project("url", project.url)) == Project:
        raise HTTPException(status_code=404, detail="Project is already in use")

    
    project_dict = dict(project)

    del project_dict["id"]

    id = db_client.projects.insert_one(project_dict).inserted_id
    return search_project("_id", id)



@router.put("/", response_model=Project)
async def update_project(project: Project):
    try:
        if not type(search_project("_id", ObjectId(project.id))) == Project:
            raise HTTPException(status_code=404, detail="Project not found")
    except:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        if not type(search_user("_id", ObjectId(project.id_user))) == User:
            raise HTTPException(status_code=404, detail="User not found")
    except:
        raise HTTPException(status_code=404, detail="User not found")


    same_project = search_project("url", project.url)
    if type(same_project) == Project and same_project.id != project.id:
        raise HTTPException(status_code=404, detail="This project is already in use") 

    project_dict = dict(project)
    del project_dict["id"]

    db_client.projects.find_one_and_replace({ "_id": ObjectId(project.id)}, project_dict)  

    return search_project("_id", ObjectId(project.id))


@router.delete("/{id}", status_code=204)
async def delete_project(id: str):
    try: 
        project_eliminated = db_client.projects.find_one_and_delete({"_id": ObjectId(id)}) 
    except:
        raise HTTPException(status_code=404, detail="Project not found")

    if not project_eliminated:
        raise HTTPException(status_code=404, detail="Project not found")