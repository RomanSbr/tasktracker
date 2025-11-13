from fastapi import APIRouter

from app.api.v1.endpoints import auth, tasks, projects, comments, organizations, workflows, permission_schemes, sprints

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
api_router.include_router(workflows.router, tags=["workflows"])
api_router.include_router(permission_schemes.router, tags=["permission-schemes"])
api_router.include_router(sprints.router, tags=["sprints"])
