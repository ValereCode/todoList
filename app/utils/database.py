from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from dotenv import  load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from ..models.task_model import Task

load_dotenv()

@asynccontextmanager
async def connect_database(app: FastAPI):
    print("DATABASE_URL:", settings.database_url)  # Vérifie si la variable est bien chargée

    try:
        client = AsyncIOMotorClient(settings.database_url)
        db = client.get_database()
        ping_response = await db.command("ping")  # Vérifie si MongoDB répond
        print("MongoDB Ping Response:", ping_response)
    except Exception as e:
        print("Error connecting to MongoDB:", str(e))
        raise Exception("Failed to connect to MongoDB")

    await init_beanie(database=client["elom_shop"], document_models=[Task])
    print("Beanie initialized successfully")
    yield
    print("Shutdown complete")

app = FastAPI(lifespan=connect_database,docs_url="/")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)