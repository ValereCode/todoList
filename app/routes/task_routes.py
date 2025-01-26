# Purpose: Define the routes for the Task model
import traceback
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
        return tasks
    except Exception as e:
        error_message = traceback.format_exc()  # Capture l'erreur complète
        print("Error fetching tasks:", error_message)
        raise HTTPException(status_code=500, detail=error_message)

@router.post("", response_model=Task)
async def create_task(task: Task):
    await Task.insert_one(task)
    return task