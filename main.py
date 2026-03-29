# Imports your classes from pawpal_system.py.
from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler, Frequency

# Creates an Owner and at least two Pets.
owner = Owner(id=1, name="Alex")

dog = Pet(id=1, name="Buddy", species="Dog", age=3)
cat = Pet(id=2, name="Luna",  species="Cat", age=5)

owner.add_pet(dog)
owner.add_pet(cat)

# Adds at least three Tasks with different times to those pets.
today = datetime.now().replace(second=0, microsecond=0)

dog.add_task(Task(
    id=1,
    description="Morning walk",
    due_time=today.replace(hour=7, minute=0),
    duration_mins=30,
    frequency=Frequency.DAILY,
))

dog.add_task(Task(
    id=2,
    description="Evening feeding",
    due_time=today.replace(hour=18, minute=0),
    duration_mins=15,
    frequency=Frequency.DAILY,
))

cat.add_task(Task(
    id=3,
    description="Vet checkup",
    due_time=today.replace(hour=10, minute=30),
    duration_mins=45,
    frequency=Frequency.ONCE,
))

cat.add_task(Task(
    id=4,
    description="Brush fur",
    due_time=today.replace(hour=14, minute=0),
    duration_mins=20,
    frequency=Frequency.WEEKLY,
))

# Prints a "Today's Schedule" to the terminal.
scheduler = Scheduler()
scheduler.add_owner(owner)

print("=" * 40)
print("        TODAY'S SCHEDULE")
print("=" * 40)

upcoming = scheduler.get_upcoming_tasks()

if not upcoming:
    print("No upcoming tasks for today.")
else:
    for pet_name, task in upcoming:
        time_str = task.due_time.strftime("%I:%M %p")
        status = "[ ]"
        print(f"{time_str}  {status}  [{pet_name}] {task.description} "
              f"({task.duration_mins} min | {task.frequency.value})")

print("=" * 40)
