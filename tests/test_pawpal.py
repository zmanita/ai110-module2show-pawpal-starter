import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
from pawpal_system import Frequency, Task, Pet, Scheduler, Owner


def test_mark_complete_changes_status():
    """Verify that mark_complete() changes task is_completed status from False to True."""
    # Task Completion: verify mark_complete() changes is_completed to True
    task = Task(id=1, description="Walk", due_time=datetime(2026, 1, 1, 9, 0))
    assert task.is_completed is False
    task.mark_complete()
    assert task.is_completed is True


def test_add_task_increases_pet_task_count():
    """Verify that adding a task to a pet increases the pet's task count."""
    # Task Addition: verify adding a task increases the pet's task count
    pet = Pet(id=1, name="Buddy", species="Dog", age=3)
    assert len(pet.tasks) == 0
    task = Task(id=1, description="Feed", due_time=datetime(2026, 1, 1, 8, 0))
    pet.add_task(task)
    assert len(pet.tasks) == 1

def test_sorting_tasks_by_due_time():
    """Verify that sorting tasks by due time orders them correctly."""
    # Task Sorting: verify sorting tasks by due time orders them correctly
    pet = Pet(id=1, name="Buddy", species="Dog", age=3)
    task1 = Task(id=1, description="Feed", due_time=datetime(2026, 1, 1, 8, 0))
    task2 = Task(id=2, description="Walk", due_time=datetime(2026, 1, 1, 9, 0))
    task3 = Task(id=3, description="Vet visit", due_time=datetime(2026, 1, 1, 7, 0))
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    sorted_tasks = pet.get_tasks_sorted_by_due_time()
    assert sorted_tasks[0].description == "Vet visit"
    assert sorted_tasks[1].description == "Feed"
    assert sorted_tasks[2].description == "Walk"


def test_recurring_task_mark_complete_creates_new_task():
    """Verify that marking a daily task complete creates a new task for the following day."""
    scheduler = Scheduler()
    owner = Owner(id=1, name="Test")
    pet = Pet(id=1, name="Buddy", species="Dog", age=3)
    task = Task(id=1, description="Feed", due_time=datetime(2026, 1, 1, 8, 0), frequency=Frequency.DAILY)
    owner.add_pet(pet)
    scheduler.add_owner(owner)
    pet.add_task(task)
    scheduler.complete_task(task.id)
    assert len(pet.tasks) == 2
    assert pet.tasks[1].due_time == datetime(2026, 1, 2, 8, 0)
    
def test_conflicting_tasks():
    """Verify that the system identifies conflicting tasks based on due times."""
    pet = Pet(id=1, name="Buddy", species="Dog", age=3)
    task1 = Task(id=1, description="Feed", due_time=datetime(2026, 1, 1, 8, 0))
    task2 = Task(id=2, description="Walk", due_time=datetime(2026, 1, 1, 8, 10))
    pet.add_task(task1)
    pet.add_task(task2)
    assert pet.has_conflicting_tasks() is True

def test_non_conflicting_tasks():
    """Verify that the system identifies non-conflicting tasks based on due times."""
    pet = Pet(id=1, name="Buddy", species="Dog", age=3)
    task1 = Task(id=1, description="Feed", due_time=datetime(2026, 1, 1, 8, 0), duration_mins=30)
    task2 = Task(id=2, description="Walk", due_time=datetime(2026, 1, 1, 9, 0), duration_mins=30)
    pet.add_task(task1)
    pet.add_task(task2)
    assert pet.has_conflicting_tasks() is False