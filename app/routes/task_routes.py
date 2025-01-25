# Purpose: Define the routes for the Task model

from fastapi import APIRouter
from app.models.task_model import Task


router = APIRouter(
    prefix='/tasks',
    tags=['It will be remove later']
)


@router.get("/t")
async def root():
    return {
        "key": "12345",
        "activity": "Hiking",
        "type": "recreational",
        "participants": 4,
        "price": 0.0
    }


@router.get("", response_model=list[Task])
async def get_tasks():
    return await Task.find().to_list()


@router.post("", response_model=Task)
async def create_task(task: Task):
    await Task.insert_one(task)
    return task