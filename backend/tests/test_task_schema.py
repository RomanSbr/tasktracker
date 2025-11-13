from uuid import uuid4

import pytest

from app.schemas import task as task_schema


def test_task_create_defaults():
    payload = task_schema.TaskCreate(
        project_id=uuid4(),
        title="Implement RBAC",
    )

    assert payload.status == task_schema.TaskStatus.BACKLOG
    assert payload.priority == task_schema.TaskPriority.MEDIUM
    assert payload.type == task_schema.TaskType.TASK
    assert payload.tags == []


def test_task_create_tags_default_is_not_shared():
    payload_one = task_schema.TaskCreate(project_id=uuid4(), title="Story One")
    payload_two = task_schema.TaskCreate(project_id=uuid4(), title="Story Two")

    payload_one.tags.append("backend")

    assert payload_two.tags == []


@pytest.mark.parametrize(
    "status",
    [
        task_schema.TaskStatus.BACKLOG,
        task_schema.TaskStatus.TODO,
        task_schema.TaskStatus.IN_PROGRESS,
        task_schema.TaskStatus.REVIEW,
        task_schema.TaskStatus.TESTING,
        task_schema.TaskStatus.DONE,
        task_schema.TaskStatus.CANCELLED,
    ],
)
def test_task_status_enum_contains_all_columns(status):
    # Каждое значение перечисления должно иметь строковое представление (используется во фронте и миграциях).
    assert isinstance(status.value, str)
    assert status.value
