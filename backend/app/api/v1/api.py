from fastapi import APIRouter

from app.api.v1.endpoints import auth, tasks, projects, comments

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
