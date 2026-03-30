import streamlit as st

# Step 1: Import classes from our backend
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Step 2: Session state "vault" ─────────────────────────────────────────────
# Streamlit reruns the script on every interaction, so we store the Owner
# object in st.session_state so it persists across reruns.

if "owner" not in st.session_state:
    st.session_state.owner = None   # created once the user submits the form

# ── Owner setup ───────────────────────────────────────────────────────────────

st.subheader("Owner Info")

with st.form("owner_form"):
    owner_name    = st.text_input("Your name", value="Jordan")
    available_time = st.number_input("Time available today (minutes)", min_value=10, max_value=480, value=90)
    submitted = st.form_submit_button("Save owner")

if submitted:
    # Create (or recreate) the Owner and wipe any pets from a previous session
    st.session_state.owner = Owner(owner_name, int(available_time))
    st.success(f"Owner '{owner_name}' saved with {available_time} min budget.")

if st.session_state.owner is None:
    st.info("Fill in your name and time budget above, then click Save owner to begin.")
    st.stop()   # nothing else can work without an owner

owner: Owner = st.session_state.owner

# ── Step 3a: Add a pet ────────────────────────────────────────────────────────

st.divider()
st.subheader("Add a Pet")

with st.form("pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species  = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"])
    add_pet  = st.form_submit_button("Add pet")

if add_pet:
    # Step 3: call owner.addPet() — wires the UI action to our class method
    pet = Pet(pet_name, species)
    owner.addPet(pet)
    st.success(f"Added {species} named '{pet_name}'.")

pets = owner.getPets()
if pets:
    st.write("**Registered pets:**", ", ".join(f"{p.name} ({p.species})" for p in pets))

# ── Step 3b: Add a task ───────────────────────────────────────────────────────

st.divider()
st.subheader("Add a Task")

if not pets:
    st.info("Add at least one pet before adding tasks.")
else:
    with st.form("task_form"):
        target_pet  = st.selectbox("For which pet?", [p.name for p in pets])
        task_desc   = st.text_input("Task description", value="Morning walk")
        duration    = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
        frequency   = st.selectbox("Frequency", ["daily", "weekly", "as-needed"])
        priority    = st.selectbox("Priority", ["high", "medium", "low"])
        add_task    = st.form_submit_button("Add task")

    if add_task:
        # Find the chosen pet and call pet.addTask() — Step 3 wiring
        chosen_pet = next(p for p in pets if p.name == target_pet)
        chosen_pet.addTask(Task(task_desc, int(duration), frequency, priority))
        st.success(f"Task '{task_desc}' added to {target_pet}.")

    # Show current tasks per pet
    for pet in pets:
        tasks = pet.getTasks()
        if tasks:
            st.markdown(f"**{pet.name}'s tasks:**")
            st.table([
                {"Description": t.description, "Duration (min)": t.duration,
                 "Frequency": t.frequency, "Priority": t.priority}
                for t in tasks
            ])

# ── Generate schedule ─────────────────────────────────────────────────────────

st.divider()
st.subheader("Generate Schedule")

if st.button("Generate schedule"):
    all_tasks = owner.getAllTasks()
    if not all_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(owner)
        scheduler.generatePlan()

        schedule = scheduler.getSchedule()
        st.success(scheduler.getSummary())

        if schedule:
            st.markdown("### Today's Plan")
            st.table([
                {"#": i + 1, "Task": t.description, "Duration (min)": t.duration, "Priority": t.priority}
                for i, t in enumerate(schedule)
            ])

        with st.expander("Scheduling Reasoning"):
            st.text(scheduler.getReasoning())
