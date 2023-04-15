from fastapi import APIRouter, HTTPException
from db.models.user import Skill, User
from db.client import db_client
from bson import ObjectId
from searcher import search_skills, search_user, search_skill

router = APIRouter(
    prefix="/skills",
    tags=["skills"],
    responses={404: {"message": "No encontrado"}})




@router.get("/{id_user}", response_model=list[Skill])
async def get_user_skills(id_user):
    user_skills = search_skills(id_user)

    if len(user_skills) <= 0:
        raise HTTPException(
            status_code=404, detail="The user doesn't exist or there aren't skills")

    return user_skills

@router.post("/", response_model=Skill, status_code=201)
async def create_skill(skill: Skill):
    try:
        if not type(search_user("_id", ObjectId(skill.id_user))) == User:
            raise HTTPException(status_code=404, detail="User not found")
    except:
        raise HTTPException(status_code=404, detail="User not found")

    skill_dict = dict(skill)

    del skill_dict["id"]

    id = db_client.skills.insert_one(skill_dict).inserted_id
    return search_skill("_id", id)



@router.put("/", response_model=Skill)
async def update_skill(skill: Skill):
    try:
        if not type(search_skill("_id", ObjectId(skill.id))) == Skill:
            raise HTTPException(status_code=404, detail="skill not found")
    except:
        raise HTTPException(status_code=404, detail="skill not found")
    
    try:
        if not type(search_user("_id", ObjectId(skill.id_user))) == User:
            raise HTTPException(status_code=404, detail="User not found")
    except:
        raise HTTPException(status_code=404, detail="User not found")


    skill_dict = dict(skill)
    del skill_dict["id"]

    db_client.skills.find_one_and_replace({ "_id": ObjectId(skill.id)}, skill_dict)  

    return search_skill("_id", ObjectId(skill.id))


@router.delete("/{id}", status_code=204)
async def delete_skill(id: str):
    try: 
        skill_eliminated = db_client.skills.find_one_and_delete({"_id": ObjectId(id)}) 
    except:
        raise HTTPException(status_code=404, detail="skill not found")

    if not skill_eliminated:
        raise HTTPException(status_code=404, detail="skill not found")