from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Task:
    id: int
    description: str
    due_time: datetime
    duration_mins: int = 15
    is_completed: bool = False
    frequency: str = "Once"  # "Once", "Daily", "Weekly"

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    id: int
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass


@dataclass
class Scheduler:
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> List[tuple]:
        pass

    def get_upcoming_tasks(self) -> List[tuple]:
        pass

    def check_conflicts(self, new_task: Task) -> bool:
        pass

    def generate_recurring_tasks(self) -> None:
        pass
