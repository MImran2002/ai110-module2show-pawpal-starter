from pawpal_system import Owner, Pet, Task, Scheduler

# ── Setup ─────────────────────────────────────────────────────────────────────

owner = Owner("Alex", available_time=90)

# Pet 1 — dog
buddy = Pet("Buddy", "dog")
buddy.addTask(Task("Morning walk",     30, "daily",     "high"))
buddy.addTask(Task("Flea medication",  10, "weekly",    "medium"))
buddy.addTask(Task("Teeth brushing",   15, "as-needed", "low"))

# Pet 2 — cat
luna = Pet("Luna", "cat")
luna.addTask(Task("Feed Luna",         10, "daily",     "high"))
luna.addTask(Task("Grooming session",  20, "weekly",    "medium"))

owner.addPet(buddy)
owner.addPet(luna)

# ── Generate plan ─────────────────────────────────────────────────────────────

scheduler = Scheduler(owner)
scheduler.generatePlan()

# ── Display ───────────────────────────────────────────────────────────────────

print("=" * 50)
print("        TODAY'S SCHEDULE")
print(f"        Owner: {owner.name}  |  Budget: {owner.available_time} min")
print("=" * 50)

schedule = scheduler.getSchedule()
if not schedule:
    print("  No tasks scheduled today.")
else:
    for i, task in enumerate(schedule, start=1):
        status = "[DONE]" if task.isCompleted else "[ ]"
        print(f"  {i}. {status} {task.description:<25} {task.duration} min  ({task.priority})")

print("-" * 50)
print(f"  {scheduler.getSummary()}")
print()
print("Reasoning:")
for line in scheduler.getReasoning().splitlines():
    print(f"  {line}")
print("=" * 50)
