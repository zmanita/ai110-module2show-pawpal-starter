# Imports your classes from pawpal_system.py.
from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler, Frequency

# Creates an Owner and at least two Pets.
owner = Owner(id=1, name="Alex")

dog = Pet(id=1, name="Buddy", species="Dog", age=3)
cat = Pet(id=2, name="Luna",  species="Cat", age=5)

owner.add_pet(dog)
owner.add_pet(cat)

# Adds tasks OUT OF ORDER to demonstrate sorting.
today = datetime.now().replace(second=0, microsecond=0)

# Dog tasks added: evening first, then morning (intentionally out of order)
dog.add_task(Task(
    id=2,
    description="Evening feeding",
    due_time=today.replace(hour=18, minute=0),
    duration_mins=15,
    frequency=Frequency.DAILY,
))

dog.add_task(Task(
    id=1,
    description="Morning walk",
    due_time=today.replace(hour=7, minute=0),
    duration_mins=30,
    frequency=Frequency.DAILY,
))

# Cat tasks added: afternoon first, then morning (intentionally out of order)
cat.add_task(Task(
    id=4,
    description="Brush fur",
    due_time=today.replace(hour=14, minute=0),
    duration_mins=20,
    frequency=Frequency.WEEKLY,
))

cat.add_task(Task(
    id=3,
    description="Vet checkup",
    due_time=today.replace(hour=10, minute=30),
    duration_mins=45,
    frequency=Frequency.ONCE,
))

# Mark one task complete to demonstrate filter_by_completion.
scheduler = Scheduler()
scheduler.add_owner(owner)
scheduler.complete_task(1)  # Mark "Morning walk" as done

# ── 1. sort_by_time ──────────────────────────────────────────────────────────
print("=" * 40)
print("   ALL TASKS SORTED BY TIME")
print("=" * 40)

for pet_name, task in scheduler.sort_by_time():
    time_str = task.due_time.strftime("%I:%M %p")
    status = "[x]" if task.is_completed else "[ ]"
    print(f"{time_str}  {status}  [{pet_name}] {task.description} "
          f"({task.duration_mins} min | {task.frequency.value})")

# ── 2. filter_by_pet ─────────────────────────────────────────────────────────
print()
for pet_name in ("Buddy", "Luna"):
    print(f"{'=' * 40}")
    print(f"   TASKS FOR {pet_name.upper()}")
    print(f"{'=' * 40}")
    for name, task in scheduler.filter_by_pet(pet_name):
        time_str = task.due_time.strftime("%I:%M %p")
        status = "[x]" if task.is_completed else "[ ]"
        print(f"{time_str}  {status}  {task.description} "
              f"({task.duration_mins} min | {task.frequency.value})")

# ── 3. filter_by_completion ───────────────────────────────────────────────────
print()
print("=" * 40)
print("   COMPLETED TASKS")
print("=" * 40)
done = scheduler.filter_by_completion(completed=True)
if done:
    for pet_name, task in done:
        time_str = task.due_time.strftime("%I:%M %p")
        print(f"{time_str}  [x]  [{pet_name}] {task.description}")
else:
    print("No completed tasks.")

print()
print("=" * 40)
print("   PENDING TASKS")
print("=" * 40)
pending = scheduler.filter_by_completion(completed=False)
if pending:
    for pet_name, task in pending:
        time_str = task.due_time.strftime("%I:%M %p")
        print(f"{time_str}  [ ]  [{pet_name}] {task.description}")
else:
    print("All tasks complete!")

print("=" * 40)
