from db.models.user import User, Project, Skill, Service

from db.schemas.user import user_schema, projects_schema, project_schema, skills_schema, skill_schema, services_schema, service_schema

from db.client import db_client


def search_user(field: str, key):
    try:
        user_json = db_client.users.find_one({ field: key })
        return User(**user_schema(user_json))
    except:
        return {"error": "User not found"}
    

def search_projects(id_user):
    try:
        projects_json = db_client.projects.find({ "id_user": id_user })
        return projects_schema(projects_json)
    except:
        return {"error": "Projects not found"}
    
def search_project(field: str, key):
    try:
        project_json = db_client.projects.find_one({ field: key })
        return Project(**project_schema(project_json))
    except:
        return {"error": "Project not found"}
    
def search_skills(id_user):
    try:
        skills_json = db_client.skills.find({ "id_user": id_user })
        return skills_schema(skills_json)
    except:
        return {"error": "Skills not found"}
    
def search_skill(field: str, key):
    try:
        skill_json = db_client.skills.find_one({ field: key })
        return Skill(**skill_schema(skill_json))
    except:
        return {"error": "Skill not found"}
    

def search_services(id_user):
    try:
        services_json = db_client.services.find({ "id_user": id_user })
        return services_schema(services_json)
    except:
        return {"error": "Services not found"}
    
def search_service(field: str, key):
    try:
        service_json = db_client.services.find_one({ field: key })
        return Service(**service_schema(service_json))
    except:
        return {"error": "Service not found"}
    