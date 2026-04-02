from app.models.task import Task, Priority
from app.repositories import task_repository


class TaskNotFoundError(Exception):
    pass


class InvalidPriorityError(Exception):
    pass


def list_all_tasks() -> list[Task]:
    return task_repository.find_all()


def create_task(title: str, priority_value: str) -> Task:
    try:
        priority = Priority.from_value(priority_value)
    except ValueError as e:
        raise InvalidPriorityError(str(e)) from None
    try:
        task = Task(title=title, priority=priority)
    except (ValueError, TypeError) as e:
        raise ValueError(str(e)) from None
    return task_repository.save(task)


def mark_as_completed(task_id: int) -> Task:
    task = task_repository.update_completion(task_id, completed=True)
    if not task:
        raise TaskNotFoundError(f"Task {task_id} not found")
    return task


def remove_task(task_id: int) -> None:
    deleted = task_repository.delete_by_id(task_id)
    if not deleted:
        raise TaskNotFoundError(f"Task {task_id} not found")
