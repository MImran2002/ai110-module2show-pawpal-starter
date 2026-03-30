from pawpal_system import Owner, Pet, Task, Scheduler

# ── Block 1: Setup ────────────────────────────────────────────────────────────

owner = Owner("Alex", available_time=90)

buddy = Pet("Buddy", "dog")
buddy.addTask(Task("Morning walk",    30, "daily",     "high"))
buddy.addTask(Task("Flea medication", 10, "weekly",    "medium"))
buddy.addTask(Task("Teeth brushing",  15, "as-needed", "low"))
buddy.addTask(Task("Quick play",       5, "daily",     "medium"))  # short task, added out of duration order

luna = Pet("Luna", "cat")
luna.addTask(Task("Feed Luna",        10, "daily",     "high"))
luna.addTask(Task("Grooming session", 20, "weekly",    "medium"))
luna.addTask(Task("Vet check",        45, "as-needed", "high"))   # long task for conflict demo

owner.addPet(buddy)
owner.addPet(luna)

scheduler = Scheduler(owner)
scheduler.generatePlan()

# ── Block 2: Original schedule display ───────────────────────────────────────

print("=" * 55)
print("              TODAY'S SCHEDULE")
print(f"        Owner: {owner.name}  |  Budget: {owner.available_time} min")
print("=" * 55)

schedule = scheduler.getSchedule()
if not schedule:
    print("  No tasks scheduled today.")
else:
    for i, task in enumerate(schedule, start=1):
        status = "[DONE]" if task.isCompleted else "[ ]"
        print(f"  {i}. {status} {task.description:<25} {task.duration:>3} min  ({task.priority})")

print("-" * 55)
print(f"  {scheduler.getSummary()}")
print()
print("  Reasoning:")
for line in scheduler.getReasoning().splitlines():
    print(f"    {line}")

# ── Block 3: Feature 1 — Sort by duration ────────────────────────────────────

print("\n" + "=" * 55)
print("  Feature 1: Sort scheduled tasks by duration")
print("=" * 55)
sorted_tasks = scheduler.sortByDuration()
for task in sorted_tasks:
    print(f"  {task.duration:>3} min  {task.description}")

# ── Block 4: Feature 2a — Filter by status ───────────────────────────────────

print("\n" + "=" * 55)
print("  Feature 2a: Filter by status")
print("=" * 55)

pending = scheduler.filterByStatus(completed=False)
print(f"Pending tasks ({len(pending)}):")
for t in pending:
    print(f"  [ ] {t.description}")

# Mark one task complete to populate next_due
morning_walk = buddy.getTasks()[0]   # "Morning walk" (daily)
morning_walk.markComplete()

completed_tasks = scheduler.filterByStatus(completed=True)
print(f"\nCompleted tasks ({len(completed_tasks)}):")
for t in completed_tasks:
    print(f"  [X] {t.description:<25}  next_due: {t.next_due}")

# ── Block 5: Feature 2b — Filter by pet ──────────────────────────────────────

print("\n" + "=" * 55)
print("  Feature 2b: Filter by pet name")
print("=" * 55)
luna_tasks = scheduler.filterByPet("luna")
print(f"Luna's tasks ({len(luna_tasks)}):")
for t in luna_tasks:
    print(f"  {t.description}")

# ── Block 6: Feature 3 — Recurring task / next_due ───────────────────────────

print("\n" + "=" * 55)
print("  Feature 3: Recurring task automation")
print("=" * 55)
flea_task = buddy.getTasks()[1]   # "Flea medication" (weekly)
print(f"  Task:          {flea_task.description} ({flea_task.frequency})")
print(f"  Before markComplete → next_due: {flea_task.next_due}, isDueToday: {flea_task.isDueToday()}")
flea_task.markComplete()
print(f"  After  markComplete → next_due: {flea_task.next_due}, isDueToday: {flea_task.isDueToday()}")

# ── Block 7: Feature 4 — Conflict detection ───────────────────────────────────

print("\n" + "=" * 55)
print("  Feature 4: Conflict detection")
print("=" * 55)
# Regenerate with all tasks (including the large Vet check for Luna)
# Reset completed flags so all tasks re-enter the plan
for pet in owner.getPets():
    for t in pet.getTasks():
        t.reset()

scheduler2 = Scheduler(owner)
scheduler2.generatePlan()
print("  Scheduled tasks:")
for t in scheduler2.getSchedule():
    print(f"    {t.description:<25} {t.duration} min")

conflicts = scheduler2.detectConflicts()
print()
if conflicts:
    for warning in conflicts:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts detected.")

print("=" * 55)
