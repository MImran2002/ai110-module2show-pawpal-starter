import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Your smart daily pet care planner.")

# ── Session state ─────────────────────────────────────────────────────────────

if "owner" not in st.session_state:
    st.session_state.owner = None

# ── Owner setup ───────────────────────────────────────────────────────────────

st.subheader("Owner Info")

with st.form("owner_form"):
    owner_name     = st.text_input("Your name", value="Jordan")
    available_time = st.number_input("Time available today (minutes)", min_value=10, max_value=480, value=90)
    submitted = st.form_submit_button("Save owner")

if submitted:
    st.session_state.owner = Owner(owner_name, int(available_time))
    st.success(f"Owner '{owner_name}' saved — {available_time} min budget for today.")

if st.session_state.owner is None:
    st.info("Fill in your name and time budget above, then click **Save owner** to begin.")
    st.stop()

owner: Owner = st.session_state.owner

# ── Add a pet ─────────────────────────────────────────────────────────────────

st.divider()
st.subheader("Pets")

with st.form("pet_form"):
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"])
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    owner.addPet(Pet(pet_name, species))
    st.success(f"Added {species} '{pet_name}'.")

pets = owner.getPets()
if pets:
    st.write("**Registered pets:**", "  |  ".join(f"**{p.name}** ({p.species})" for p in pets))

# ── Add a task ────────────────────────────────────────────────────────────────

st.divider()
st.subheader("Tasks")

if not pets:
    st.info("Add at least one pet before adding tasks.")
else:
    with st.form("task_form"):
        col1, col2 = st.columns(2)
        with col1:
            target_pet = st.selectbox("For which pet?", [p.name for p in pets])
            task_desc  = st.text_input("Task description", value="Morning walk")
            frequency  = st.selectbox("Frequency", ["daily", "weekly", "as-needed"])
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
            priority = st.selectbox("Priority", ["high", "medium", "low"])
        add_task = st.form_submit_button("Add task")

    if add_task:
        chosen_pet = next(p for p in pets if p.name == target_pet)
        chosen_pet.addTask(Task(task_desc, int(duration), frequency, priority))
        st.success(f"Task '{task_desc}' added to {target_pet}.")

    # Show tasks per pet
    for pet in pets:
        tasks = pet.getTasks()
        if tasks:
            st.markdown(f"**{pet.name}'s tasks:**")
            st.table([
                {
                    "Description": t.description,
                    "Duration (min)": t.duration,
                    "Frequency": t.frequency,
                    "Priority": t.priority,
                    "Done?": "✅" if t.isCompleted else "—",
                }
                for t in tasks
            ])

# ── Generate schedule ─────────────────────────────────────────────────────────

st.divider()
st.subheader("Generate Schedule")

# View options shown before generating
sort_by_duration = st.checkbox("Sort results by duration (shortest first)", value=False)
filter_pet       = st.selectbox(
    "Filter schedule by pet (optional)",
    ["All pets"] + [p.name for p in pets],
)

if st.button("Generate schedule", type="primary"):
    all_tasks = owner.getAllTasks()
    if not all_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(owner)
        scheduler.generatePlan()
        schedule  = scheduler.getSchedule()

        # ── Summary banner ────────────────────────────────────────────────────
        if schedule:
            st.success(f"✅ {scheduler.getSummary()}")
        else:
            st.warning("No tasks could be scheduled within the available time.")

        # ── Conflict warnings ─────────────────────────────────────────────────
        conflicts = scheduler.detectConflicts()
        if conflicts:
            st.error("⚠️ **Scheduling conflicts detected** — review the warnings below:")
            for msg in conflicts:
                st.warning(msg)

        # ── Today's plan table ────────────────────────────────────────────────
        if schedule:
            display_tasks = schedule

            # Apply pet filter
            if filter_pet != "All pets":
                pet_obj = next((p for p in pets if p.name == filter_pet), None)
                if pet_obj:
                    pet_task_set = set(id(t) for t in pet_obj.getTasks())
                    display_tasks = [t for t in display_tasks if id(t) in pet_task_set]

            # Apply duration sort
            if sort_by_duration:
                display_tasks = scheduler.sortByDuration()
                if filter_pet != "All pets":
                    pet_task_set = set(id(t) for t in pet_obj.getTasks())
                    display_tasks = [t for t in display_tasks if id(t) in pet_task_set]

            st.markdown("### Today's Plan")

            PRIORITY_BADGE = {"high": "🔴", "medium": "🟡", "low": "🟢"}

            if display_tasks:
                st.table([
                    {
                        "#": i + 1,
                        "Task": t.description,
                        "Duration (min)": t.duration,
                        "Priority": f"{PRIORITY_BADGE.get(t.priority, '')} {t.priority}",
                        "Frequency": t.frequency,
                        "Next due": str(t.next_due) if t.next_due else "—",
                    }
                    for i, t in enumerate(display_tasks)
                ])
            else:
                st.info(f"No scheduled tasks for {filter_pet}.")

        # ── Skipped tasks ─────────────────────────────────────────────────────
        skipped = scheduler.filterByStatus(completed=False)
        skipped = [t for t in skipped if t not in schedule]
        if skipped:
            with st.expander(f"Skipped tasks ({len(skipped)}) — didn't fit in your time budget"):
                st.table([
                    {"Task": t.description, "Duration (min)": t.duration, "Priority": t.priority}
                    for t in skipped
                ])

        # ── Reasoning ─────────────────────────────────────────────────────────
        with st.expander("Scheduling reasoning"):
            st.text(scheduler.getReasoning())
