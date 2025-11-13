# Import all models here for Alembic to detect them
from app.db.session import Base
from app.models.user import User
from app.models.organization import Organization
from app.models.project import Project
from app.models.task import Task, TaskHistory, TaskDependency
from app.models.comment import Comment
from app.models.sprint import Sprint
from app.models.attachment import Attachment
from app.models.workflow import Workflow, WorkflowStatus, WorkflowTransition
from app.models.permission import PermissionScheme, PermissionSchemeRule

# Association tables
from app.models.associations import (
    user_organizations,
    project_members,
    task_watchers,
)
