from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from ..models.task_model import Task


@asynccontextmanager
async def connect_database(app: FastAPI):

    try:
        client = AsyncIOMotorClient(settings.database_url)
        db = client["elom_shop"]

        # Test de connexion
        ping_response = await db.command("ping")
        print("✅ MongoDB connecté :", ping_response)

        # Initialiser Beanie
        await init_beanie(database=db, document_models=[Task])
        print("✅ Beanie initialisé avec Task")

    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("❌ Erreur de connexion MongoDB :", error_message)
        raise Exception("Échec de connexion MongoDB: " + str(e))

    yield

