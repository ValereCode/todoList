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
    print("DATABASE_URL:", settings.database_url)  # Vérifie la variable d'env

    try:
        client = AsyncIOMotorClient(settings.database_url)
        db = client["elom_shop"]

        # Test de connexion
        ping_response = await db.command("ping")
        print("✅ MongoDB connecté :", ping_response)

        # Vérifier si la collection "tasks" existe
        collection_names = await db.list_collection_names()
        print("Collections existantes :", collection_names)
        if "tasks" not in collection_names:
            print("⚠️ Collection 'tasks' non trouvée, elle sera créée à la première insertion.")

        # Initialiser Beanie
        await init_beanie(database=db, document_models=[Task])
        print("✅ Beanie initialisé avec Task")

    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("❌ Erreur de connexion MongoDB :", error_message)
        raise Exception("Échec de connexion MongoDB: " + str(e))

    yield

app = FastAPI(lifespan=connect_database,docs_url="/")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)