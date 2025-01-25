from app.utils.database import app
from app.routes import task_routes


app.include_router(task_routes.router)