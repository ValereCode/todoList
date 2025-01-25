# Purpose: Define the routes for the Task model

from fastapi import APIRouter, HTTPException
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
    try:
        tasks = await Task.find().to_list()
        print("Tasks fetched successfully:", tasks)
        return tasks
    except Exception as e:
        print("Error fetching tasks:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=Task)
async def create_task(task: Task):
    await Task.insert_one(task)
    return task