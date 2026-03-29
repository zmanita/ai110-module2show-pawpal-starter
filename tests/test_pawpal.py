import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
from pawpal_system import Task, Pet


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
