from pydantic import Field

from beanie import Document


class Task(Document):
    title: str
    description: str
    due_date: str = Field(alias="dueDate")
    status: str
    priority: int
    created_date: str = Field(alias="createdDate")
    updated_date: str = Field(alias="updatedDate")

    class Settings:
        collection = "tasks"
