from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str]
    firstName: str
    secondName: str
    lastName: str
    mLastName: str
    birthday: str
    occupation: str
    experience: str
    languages: list
    education: str
    email: str
    phone: str
    location: str

class Service(BaseModel):
    id: Optional[str]
    id_user: str
    name: str
    title: str
    description: str

class Project(BaseModel):
    id: Optional[str]
    id_user: str
    name: str
    url: str
    gitcode: str
    img: str

class Skill(BaseModel):
    id: Optional[str]
    id_user: str
    name: str
    level: str
    icon: str





    


    
