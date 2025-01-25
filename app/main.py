from app.utils.database import connect_database
from app.routes import task_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(lifespan=connect_database,docs_url="/")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_routes.router)