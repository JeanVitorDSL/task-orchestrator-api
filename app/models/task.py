from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Task:
    title: str
    priority: Priority
    id: Optional[int] = None
    completed: bool = False
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority.value,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
