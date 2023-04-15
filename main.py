from routers import users, projects, skills, services
from fastapi import FastAPI, HTTPException

# from db.models.vocabulario import Vocabulario, Palabra

# from db.schemas.vocabulario import vocabularios_schema
# from db.client import db_client

# from buscador import search_vocabulario, search_palabras_por_vocabulario
# from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv


load_dotenv()


app = FastAPI()

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(skills.router)
app.include_router(services.router)
# app.include_router(usuarios.router)


origins = [
    "http://localhost:8080",
    # "https://vocabularios.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def api_portfolio():
    return {"API PORTFOLIO": "This a portfolio API. Web portfolio is a collection of works or projects that have been completed in the field of web design or web development, including information about the web designer or developer and their experience, as well as examples of projects they have worked on, services provided, skills and contact information"}




# uvicorn main:app --reload