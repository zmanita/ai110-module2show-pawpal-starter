# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan


## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Features

- **Sort tasks by due time** — `sort_by_time()` and `get_tasks_sorted_by_due_time()` return all tasks ordered chronologically by `due_time`, across all pets or per pet.
- **Upcoming task queue** — `get_upcoming_tasks()` filters out completed tasks and sorts the remaining ones by due time, giving a prioritized to-do list.
- **Conflict detection (per-pet)** — `has_conflicting_tasks()` uses an O(n²) pairwise overlap check on a single pet's tasks to detect scheduling collisions.
- **Conflict detection (cross-pet)** — `get_all_conflicts()` applies the same interval-overlap logic across every pet's incomplete tasks, returning all conflicting pairs.
- **Conflict warnings on scheduling** — `schedule_task()` always adds the task but returns a human-readable warning string for every overlap found (never blocks scheduling).
- **Pre-add conflict check** — `check_conflicts()` lets callers query whether a candidate task would overlap with any existing incomplete task before committing it.
- **Daily and weekly recurrence** — `generate_recurring_tasks()` walks the time window since `last_run` and backfills any missed occurrences for `DAILY` and `WEEKLY` tasks.
- **Auto-advance on completion** — `complete_task()` marks a task done and immediately schedules the next occurrence (shifted by the task's interval) for recurring tasks.
- **Filter by pet** — `filter_by_pet()` returns all tasks belonging to a named pet regardless of completion status.
- **Filter by completion status** — `filter_by_completion()` returns tasks matching a given `is_completed` boolean, enabling separate pending/done views.
- **Bulk cleanup** — `remove_completed_tasks()` prunes all completed tasks across every pet in a single pass.

## Testing PawPal+
Use this command to run tests: ``` python -m pytest ```
The tests cover:
1. Any task's is_completed status is changed from False to True once user marks it done.
2. Adding a task to a pet increases the pet's task count.
3. Sorting tasks by due time orders them correctly in pawpal_system. 
4. Marking a daily task complete creates a new task for the following day.
5. The system identifies conflicting tasks based on due times. Task1 ending at 9:30 and task2 ending at 9:30 produces a conflict.
6. The system identifies non-conflicting tasks based on due times. Task1 ending at 9:29 and task2 starting at 9:30 do not produce a conflict.

 ##📸 Demo
 <a href="/course_images/ai110/Screenshot 2026-03-29 at 10.47.17 PM" target="_blank"><img src='/Users/zarinmusarratmanita/Desktop/Spring26/AI110/ai110-module2show-pawpal-starter/Screenshot 2026-03-29 at 10.47.17 PM.png>