from dataclasses import dataclass, field
from typing import Optional

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


# ── Task ──────────────────────────────────────────────────────────────────────

@dataclass
class Task:
    """A single pet care activity."""
    description: str
    duration: int          # minutes
    frequency: str         # "daily" | "weekly" | "as-needed"
    priority: str          # "high" | "medium" | "low"
    isCompleted: bool = field(default=False)

    def markComplete(self) -> None:
        """Mark this task as done."""
        self.isCompleted = True

    def reset(self) -> None:
        """Reset completion status for a new day."""
        self.isCompleted = False

    def isDue(self) -> bool:
        """Return True if this task should be considered for today's plan."""
        if self.frequency == "daily":
            return True
        # weekly and as-needed only surface when not yet done
        return not self.isCompleted

    def getDuration(self) -> int:
        """Return the task duration in minutes."""
        return self.duration

    def getPriority(self) -> str:
        """Return the task priority level."""
        return self.priority


# ── Pet ───────────────────────────────────────────────────────────────────────

@dataclass
class Pet:
    """A pet that owns a list of care tasks."""
    name: str
    species: str
    tasks: list = field(default_factory=list)  # list[Task]

    def addTask(self, task: Task) -> None:
        """Add a task if it isn't already in the list."""
        if task not in self.tasks:
            self.tasks.append(task)

    def removeTask(self, task: Task) -> None:
        """Remove a task if present."""
        if task in self.tasks:
            self.tasks.remove(task)

    def getTasks(self) -> list:
        """Return all tasks (completed and pending)."""
        return self.tasks

    def getPendingTasks(self) -> list:
        """Return only tasks that have not been completed."""
        return [t for t in self.tasks if not t.isCompleted]


# ── Owner ─────────────────────────────────────────────────────────────────────

class Owner:
    """A pet owner who manages multiple pets and has a daily time budget."""

    def __init__(self, name: str, available_time: int):
        """
        Args:
            name: Owner's name.
            available_time: Total minutes available for pet care today.
        """
        self.name = name
        self.available_time = available_time
        self._pets: list = []  # list[Pet]

    def addPet(self, pet: Pet) -> None:
        """Add a pet if not already registered."""
        if pet not in self._pets:
            self._pets.append(pet)

    def getPets(self) -> list:
        """Return all registered pets."""
        return self._pets

    def getAllTasks(self) -> list:
        """Return a flat list of every task across all pets."""
        return [task for pet in self._pets for task in pet.getTasks()]


# ── Scheduler ─────────────────────────────────────────────────────────────────

class Scheduler:
    """
    The scheduling brain.

    Retrieves due tasks from all of an owner's pets, sorts them by priority,
    and greedily fits them into the owner's available time budget.
    """

    def __init__(self, owner: Owner):
        """Initialise the scheduler with an owner whose pets and tasks will be planned."""
        self.owner = owner
        self._schedule: list = []   # tasks that fit
        self._excluded: list = []   # tasks that didn't fit
        self._reasoning: str = ""
        self._summary: str = ""

    def generatePlan(self) -> None:
        """Build a prioritised daily schedule within the owner's time budget."""
        # Reset state
        self._schedule = []
        self._excluded = []
        reasoning_lines = []

        # 1. Collect all pending, due tasks across every pet
        due_tasks = [
            task
            for pet in self.owner.getPets()
            for task in pet.getPendingTasks()
            if task.isDue()
        ]

        # 2. Sort high → medium → low (unknown priority falls to the end)
        sorted_tasks = sorted(
            due_tasks,
            key=lambda t: PRIORITY_ORDER.get(t.priority, 99)
        )

        # 3. Greedy fit
        time_remaining = self.owner.available_time

        for task in sorted_tasks:
            if task.duration <= time_remaining:
                self._schedule.append(task)
                time_remaining -= task.duration
                reasoning_lines.append(
                    f"INCLUDED: '{task.description}' "
                    f"({task.duration} min, {task.priority} priority) "
                    f"— fits with {time_remaining} min remaining."
                )
            else:
                self._excluded.append(task)
                reasoning_lines.append(
                    f"EXCLUDED: '{task.description}' "
                    f"({task.duration} min, {task.priority} priority) "
                    f"— needs {task.duration} min but only {time_remaining} min left."
                )

        # 4. Build reasoning and summary
        self._reasoning = "\n".join(reasoning_lines) if reasoning_lines else "No tasks to schedule."

        total_scheduled = sum(t.duration for t in self._schedule)
        self._summary = (
            f"Scheduled {len(self._schedule)} task(s) totalling {total_scheduled} min "
            f"out of {self.owner.available_time} min available. "
            f"{len(self._excluded)} task(s) were skipped."
        )

    def getSchedule(self) -> list:
        """Return the list of scheduled tasks (call generatePlan first)."""
        return self._schedule

    def getReasoning(self) -> str:
        """Return a line-by-line explanation of scheduling decisions."""
        return self._reasoning

    def getSummary(self) -> str:
        """Return a one-line summary of the generated plan."""
        return self._summary
