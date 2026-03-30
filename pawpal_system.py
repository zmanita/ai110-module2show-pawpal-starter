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
    
    def get_tasks_sorted_by_due_time(self) -> List[Task]:
        return sorted(self.tasks, key=lambda t: t.due_time)

    def has_conflicting_tasks(self) -> bool:
        for i in range(len(self.tasks)):
            for j in range(i + 1, len(self.tasks)):
                a, b = self.tasks[i], self.tasks[j]
                end_a = a.due_time + timedelta(minutes=a.duration_mins)
                end_b = b.due_time + timedelta(minutes=b.duration_mins)
                if a.due_time < end_b and b.due_time < end_a:
                    return True
        return False


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
        # Returns True if new_task overlaps with any existing incomplete task for the pet.
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
        # For each recurring task, if its next occurrence falls between last_run and now,
        # create a new Task instance for that occurrence and add it to the pet's tasks.
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
        # Deletes all tasks marked as completed across all pets.
        for owner in self.owners:
            for pet in owner.pets:
                pet.tasks = [t for t in pet.tasks if not t.is_completed]

    def remove_task(self, task_id: int) -> None:
        for owner in self.owners:
            for pet in owner.pets:
                pet.remove_task(task_id)

    def complete_task(self, task_id: int) -> None:
        # Marks the task with the given ID as completed. If it's a recurring task, also schedules the next occurrence.
        for owner in self.owners:
            for pet in owner.pets:
                for task in pet.tasks:
                    if task.id != task_id:
                        continue
                    task.mark_complete()
                    if task.frequency == Frequency.DAILY:
                        interval = timedelta(days=1)
                    elif task.frequency == Frequency.WEEKLY:
                        interval = timedelta(weeks=1)
                    else:
                        return
                    next_id = max(t.id for _, t in self.get_all_tasks()) + 1
                    pet.add_task(Task(
                        id=next_id,
                        description=task.description,
                        due_time=task.due_time + interval,
                        duration_mins=task.duration_mins,
                        frequency=task.frequency,
                    ))
                    return
    
    def schedule_task(self, pet: Pet, task: Task) -> str:
        # Adds the task and returns a warning string for every overlap found.
        # Never raises — the task is always scheduled regardless of conflicts.
        warnings = []
        new_end = task.due_time + timedelta(minutes=task.duration_mins)
        for name, existing in self.get_all_tasks():
            if existing.is_completed:
                continue
            existing_end = existing.due_time + timedelta(minutes=existing.duration_mins)
            if task.due_time < existing_end and existing.due_time < new_end:
                warnings.append(
                    f"WARNING: '{task.description}' ({pet.name}, "
                    f"{task.due_time.strftime('%I:%M %p')}-{new_end.strftime('%I:%M %p')}) "
                    f"overlaps with '{existing.description}' ({name}, "
                    f"{existing.due_time.strftime('%I:%M %p')}-{existing_end.strftime('%I:%M %p')})"
                )
        pet.add_task(task)
        return "\n".join(warnings)

    def get_all_conflicts(self) -> List[tuple[tuple[str, Task], tuple[str, Task]]]:
        # Returns every pair of incomplete tasks whose time windows overlap,
        # including tasks belonging to different pets.
        all_tasks = [(name, task) for name, task in self.get_all_tasks()
                     if not task.is_completed]
        conflicts = []
        for i in range(len(all_tasks)):
            for j in range(i + 1, len(all_tasks)):
                _, task_a = all_tasks[i]
                _, task_b = all_tasks[j]
                end_a = task_a.due_time + timedelta(minutes=task_a.duration_mins)
                end_b = task_b.due_time + timedelta(minutes=task_b.duration_mins)
                if task_a.due_time < end_b and task_b.due_time < end_a:
                    conflicts.append((all_tasks[i], all_tasks[j]))
        return conflicts

    def sort_by_time(self) -> List[tuple[str, Task]]:
        # Returns all tasks sorted by their due_time, regardless of pet or completion status.
        return sorted(self.get_all_tasks(), key=lambda pair: pair[1].due_time)
    
    def filter_by_pet(self, pet_name: str) -> List[tuple[str, Task]]:
        # Returns all tasks belonging to the pet with the given name, regardless of completion status.
        return [(name, task) for name, task in self.get_all_tasks() if name == pet_name]
    
    def filter_by_completion(self, completed: bool) -> List[tuple[str, Task]]:
        # Returns all tasks filtered by their completion status.
        return [(name, task) for name, task in self.get_all_tasks() if task.is_completed == completed]
