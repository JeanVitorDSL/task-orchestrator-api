from flask import Blueprint, request, jsonify
from app.services import task_service
from app.services.task_service import TaskNotFoundError, InvalidPriorityError

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@task_bp.get("/")
def list_tasks():
    tasks = task_service.list_all_tasks()
    return jsonify([t.to_dict() for t in tasks]), 200


@task_bp.post("/")
def create_task():
    body = request.get_json(silent=True) or {}
    title = body.get("title", "")
    priority = body.get("priority", "medium")
    try:
        task = task_service.create_task(title, priority)
        return jsonify(task.to_dict()), 201
    except (ValueError, InvalidPriorityError) as e:
        return jsonify({"error": str(e)}), 400


@task_bp.patch("/<int:task_id>/complete")
def complete_task(task_id: int):
    try:
        task = task_service.mark_as_completed(task_id)
        return jsonify(task.to_dict()), 200
    except TaskNotFoundError as e:
        return jsonify({"error": str(e)}), 404


@task_bp.delete("/<int:task_id>")
def delete_task(task_id: int):
    try:
        task_service.remove_task(task_id)
        return "", 204
    except TaskNotFoundError as e:
        return jsonify({"error": str(e)}), 404
