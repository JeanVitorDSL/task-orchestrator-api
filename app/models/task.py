from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


TITLE_MAX_LENGTH = 255


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    @classmethod
    def from_value(cls, value: str) -> Priority:
        try:
            return cls(value.strip().lower())
        except ValueError:
            valid = [p.value for p in cls]
            raise ValueError(
                f"Invalid priority '{value}'. Must be one of: {valid}"
            )


@dataclass
class Task:
    title: str
    priority: Priority
    id: Optional[int] = None
    completed: bool = False
    created_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if not isinstance(self.title, str):
            raise TypeError(f"title must be a string, got {type(self.title).__name__}")
        self.title = self.title.strip()
        if not self.title:
            raise ValueError("title cannot be empty")
        if len(self.title) > TITLE_MAX_LENGTH:
            raise ValueError(
                f"title exceeds maximum length of {TITLE_MAX_LENGTH} characters"
            )
        if isinstance(self.priority, str):
            self.priority = Priority.from_value(self.priority)
        if not isinstance(self.priority, Priority):
            raise TypeError(
                f"priority must be a Priority enum, got {type(self.priority).__name__}"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority.value,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Task:
        return cls(
            id=data.get("id"),
            title=data.get("title", ""),
            priority=Priority.from_value(data.get("priority", "medium")),
            completed=data.get("completed", False),
            created_at=_parse_datetime(data.get("created_at")),
        )

    def __repr__(self) -> str:
        return (
            f"Task(id={self.id}, title={self.title!r}, "
            f"priority={self.priority.value}, completed={self.completed})"
        )


def _parse_datetime(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        dt = datetime.fromisoformat(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    raise TypeError(f"Cannot parse datetime from {type(value).__name__}")
