from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List
from enum import Enum


class Frequency(Enum):
    ONCE = "Once"
    DAILY = "Daily"
    WEEKLY = "Weekly"


@dataclass
class Task:
    # Represents a single activity (description, time, frequency, completion status)
    id: int
    description: str
    due_time: datetime
    duration_mins: int = 15
    is_completed: bool = False
    frequency: Frequency = Frequency.ONCE

    def mark_complete(self) -> None:
        self.is_completed = True


@dataclass
class Pet:
    # Stores pet details and a list of tasks.
    id: int
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task_id: int) -> None:
        self.tasks = [t for t in self.tasks if t.id != task_id]


@dataclass
class Owner:
    # Manages multiple pets and provides access to all their tasks.
    id: int
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def remove_pet(self, pet_id: int) -> None:
        self.pets = [p for p in self.pets if p.id != pet_id]


@dataclass
class Scheduler:
    # The "Brain" that retrieves, organizes, and manages tasks across pets.
    owners: List[Owner] = field(default_factory=list)

    def add_owner(self, owner: Owner) -> None:
        self.owners.append(owner)

    def get_all_tasks(self) -> List[tuple[str, Task]]:
        result = []
        for owner in self.owners:
            for pet in owner.pets:
                for task in pet.tasks:
                    result.append((pet.name, task))
        return result

    def get_upcoming_tasks(self) -> List[tuple[str, Task]]:
        incomplete = [(name, task) for name, task in self.get_all_tasks()
                      if not task.is_completed]
        return sorted(incomplete, key=lambda pair: pair[1].due_time)

    def check_conflicts(self, pet: Pet, new_task: Task) -> bool:
        new_end = new_task.due_time + timedelta(minutes=new_task.duration_mins)
        for task in pet.tasks:
            if task.is_completed:
                continue
            task_end = task.due_time + timedelta(minutes=task.duration_mins)
            # Two tasks conflict when their time windows overlap
            if new_task.due_time < task_end and task.due_time < new_end:
                return True
        return False

    def generate_recurring_tasks(self, last_run: datetime) -> None:
        now = datetime.now()
        new_tasks: List[tuple[Pet, Task]] = []
        next_id = max((t.id for _, t in self.get_all_tasks()), default=0) + 1

        for owner in self.owners:
            for pet in owner.pets:
                for task in pet.tasks:
                    if task.frequency == Frequency.DAILY:
                        interval = timedelta(days=1)
                    elif task.frequency == Frequency.WEEKLY:
                        interval = timedelta(weeks=1)
                    else:
                        continue

                    next_due = task.due_time + interval
                    while last_run < next_due <= now:
                        new_tasks.append((pet, Task(
                            id=next_id,
                            description=task.description,
                            due_time=next_due,
                            duration_mins=task.duration_mins,
                            frequency=task.frequency,
                        )))
                        next_id += 1
                        next_due += interval

        for pet, task in new_tasks:
            pet.add_task(task)

    def remove_completed_tasks(self) -> None:
        for owner in self.owners:
            for pet in owner.pets:
                pet.tasks = [t for t in pet.tasks if not t.is_completed]

    def remove_task(self, task_id: int) -> None:
        for owner in self.owners:
            for pet in owner.pets:
                pet.remove_task(task_id)

    def complete_task(self, task_id: int) -> None:
        for _, task in self.get_all_tasks():
            if task.id == task_id:
                task.mark_complete()
                return
