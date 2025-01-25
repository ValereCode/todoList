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
    print(settings.database_url)
    # Create Motor client
    client = AsyncIOMotorClient(settings.database_url)
    # ****************************************************#
    ping_response = await client.elom_shop.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        print("Connected to database cluster.")
    # ****************************************************#
    # Initialize beanie with documents classes and a database
    await init_beanie(
        database=client.elom_shop,
        document_models=[Task]
    )
    print("Startup complete")
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