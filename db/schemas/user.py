def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "firstName": user["firstName"],
        "secondName": user["secondName"],
        "lastName": user["lastName"],
        "mLastName": user["mLastName"],
        "birthday": user["birthday"],
        "occupation": user["occupation"],
        "experience": user["experience"],
        "languages":  user["languages"],
        "education": user["education"],
        "email": user["email"],
        "phone": user["phone"],
        "location": user["location"],
    }


def users_schema(users) -> list:
    return [user_schema(user) for user in users]


def service_schema(service) -> dict:
    return {
        "id": str(service["_id"]),
        "id_user": service["id_user"],
        "name": service["name"],
        "title": service["title"],
        "description": service["description"],
    }

def services_schema(services) -> list:
    return [service_schema(service) for service in services]



def project_schema(project) -> dict:
    return {
        "id": str(project["_id"]),
        "id_user": project["id_user"],
        "name": project["name"],
        "url": project["url"],
        "gitcode": project["gitcode"],
        "img": project["img"]
    }

def projects_schema(projects) -> list:
    return [project_schema(project) for project in projects]

def skill_schema(skill) -> dict:
    return {
        "id": str(skill["_id"]),
        "id_user": skill["id_user"],
        "name": skill["name"],
        "level": skill["level"],
        "icon": skill["icon"],
    }

def skills_schema(skills) -> list:
    return [skill_schema(skill) for skill in skills]






