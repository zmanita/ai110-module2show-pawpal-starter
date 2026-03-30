import streamlit as st
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler, Frequency

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Persist Owner, Scheduler, and ID counters across reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner(id=1, name="")
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()
    st.session_state.scheduler.add_owner(st.session_state.owner)
if "next_pet_id" not in st.session_state:
    st.session_state.next_pet_id = 1
if "next_task_id" not in st.session_state:
    st.session_state.next_task_id = 1

st.title("🐾 PawPal+")

st.divider()

# ── Owner ────────────────────────────────────────────────────────────────────
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
st.session_state.owner.name = owner_name

# ── Add a Pet ────────────────────────────────────────────────────────────────
st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])

if st.button("Add pet"):
    new_pet = Pet(
        id=st.session_state.next_pet_id,
        name=pet_name,
        species=species,
        age=0,
    )
    st.session_state.owner.add_pet(new_pet)
    st.session_state.next_pet_id += 1
    st.success(f"Added {pet_name} the {species}!")

if st.session_state.owner.pets:
    st.write("Your pets:")
    st.table([{"Name": p.name, "Species": p.species} for p in st.session_state.owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ── Add a Task ───────────────────────────────────────────────────────────────
st.subheader("Add a Task")

if not st.session_state.owner.pets:
    st.warning("Add a pet first before scheduling tasks.")
else:
    pet_names = [p.name for p in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Assign to pet", pet_names)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        freq_choice = st.selectbox("Frequency", [f.value for f in Frequency])

    due_time = st.time_input("Due time", value=datetime.now().replace(second=0, microsecond=0).time())

    if st.button("Add task"):
        target_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet_name)
        new_task = Task(
            id=st.session_state.next_task_id,
            description=task_title,
            due_time=datetime.combine(datetime.today(), due_time),
            duration_mins=int(duration),
            frequency=Frequency(freq_choice),
        )
        if st.session_state.scheduler.check_conflicts(target_pet, new_task):
            st.error(f"Conflict detected! {selected_pet_name} already has a task at that time.")
        else:
            target_pet.add_task(new_task)
            st.session_state.next_task_id += 1
            st.success(f"Added '{task_title}' to {selected_pet_name}.")

st.divider()

# ── Generate Schedule ────────────────────────────────────────────────────────
st.subheader("Today's Schedule")

# Filter controls
col_filter1, col_filter2 = st.columns(2)
with col_filter1:
    all_pet_names = [p.name for p in st.session_state.owner.pets]
    filter_pet = st.selectbox(
        "Filter by pet", ["All pets"] + all_pet_names, key="filter_pet"
    )
with col_filter2:
    filter_status = st.selectbox(
        "Filter by status", ["All", "Pending", "Completed"], key="filter_status"
    )

if st.button("Generate schedule"):
    scheduler = st.session_state.scheduler

    # Use sort_by_time() as the base sorted list
    sorted_tasks = scheduler.sort_by_time()

    # Apply pet filter via filter_by_pet()
    if filter_pet != "All pets":
        sorted_tasks = [
            (name, task) for name, task in sorted_tasks if name == filter_pet
        ]

    # Apply completion filter via filter_by_completion()
    if filter_status == "Pending":
        completed_set = {
            id(task) for _, task in scheduler.filter_by_completion(False)
        }
        sorted_tasks = [(n, t) for n, t in sorted_tasks if id(t) in completed_set]
    elif filter_status == "Completed":
        completed_set = {
            id(task) for _, task in scheduler.filter_by_completion(True)
        }
        sorted_tasks = [(n, t) for n, t in sorted_tasks if id(t) in completed_set]

    if not sorted_tasks:
        st.info("No tasks match the selected filters.")
    else:
        rows = [
            {
                "Time": task.due_time.strftime("%I:%M %p"),
                "Pet": pet_name,
                "Task": task.description,
                "Duration (min)": task.duration_mins,
                "Frequency": task.frequency.value,
                "Status": "✅ Done" if task.is_completed else "⏳ Pending",
            }
            for pet_name, task in sorted_tasks
        ]
        st.success(f"Showing {len(rows)} task(s) sorted by time.")
        st.table(rows)

    # ── Conflict Warnings ─────────────────────────────────────────────────────
    conflicts = scheduler.get_all_conflicts()
    if conflicts:
        st.markdown(
            "<p style='color:red; font-weight:bold;'>⚠️ Schedule Conflicts Detected:</p>",
            unsafe_allow_html=True,
        )
        for (name_a, task_a), (name_b, task_b) in conflicts:
            end_a = (task_a.due_time + timedelta(minutes=task_a.duration_mins)).strftime("%I:%M %p")
            end_b = (task_b.due_time + timedelta(minutes=task_b.duration_mins)).strftime("%I:%M %p")
            msg = (
                f"**'{task_a.description}'** ({name_a}, "
                f"{task_a.due_time.strftime('%I:%M %p')}–{end_a}) "
                f"overlaps with **'{task_b.description}'** ({name_b}, "
                f"{task_b.due_time.strftime('%I:%M %p')}–{end_b})"
            )
            st.markdown(
                f"<p style='color:red;'>• {msg}</p>", unsafe_allow_html=True
            )
