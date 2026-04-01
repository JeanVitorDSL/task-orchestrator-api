import psycopg2
import psycopg2.extras
from app.models.task import Task, Priority
from app.config import Config


def get_connection():
    return psycopg2.connect(Config.DATABASE_URL)


def find_all() -> list[Task]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            rows = cur.fetchall()
    return [_row_to_task(row) for row in rows]


def find_by_id(task_id: int) -> Task | None:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            row = cur.fetchone()
    return _row_to_task(row) if row else None


def save(task: Task) -> Task:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO tasks (title, priority, completed)
                VALUES (%s, %s, %s)
                RETURNING *
                """,
                (task.title, task.priority.value, task.completed),
            )
            row = cur.fetchone()
        conn.commit()
    return _row_to_task(row)


def update_completion(task_id: int, completed: bool) -> Task | None:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "UPDATE tasks SET completed = %s WHERE id = %s RETURNING *",
                (completed, task_id),
            )
            row = cur.fetchone()
        conn.commit()
    return _row_to_task(row) if row else None


def delete_by_id(task_id: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            deleted = cur.rowcount > 0
        conn.commit()
    return deleted


def _row_to_task(row: dict) -> Task:
    return Task(
        id=row["id"],
        title=row["title"],
        priority=Priority(row["priority"]),
        completed=row["completed"],
        created_at=row["created_at"],
    )