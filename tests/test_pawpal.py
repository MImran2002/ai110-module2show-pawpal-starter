import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# ── Existing tests ────────────────────────────────────────────────────────────

def test_task_completion():
    """markComplete() should set isCompleted to True."""
    task = Task("Morning walk", 30, "daily", "high")
    assert task.isCompleted is False
    task.markComplete()
    assert task.isCompleted is True


def test_task_addition_increases_pet_task_count():
    """addTask() should increase a pet's task count by 1 each time."""
    pet = Pet("Buddy", "dog")
    assert len(pet.getTasks()) == 0

    pet.addTask(Task("Walk", 30, "daily", "high"))
    assert len(pet.getTasks()) == 1

    pet.addTask(Task("Feed", 10, "daily", "high"))
    assert len(pet.getTasks()) == 2


# ── Sorting ───────────────────────────────────────────────────────────────────

def test_sort_by_duration_returns_ascending_order():
    """sortByDuration() should return tasks shortest to longest."""
    owner = Owner("Alex", available_time=120)
    pet = Pet("Buddy", "dog")
    pet.addTask(Task("Long task",   60, "daily", "high"))
    pet.addTask(Task("Short task",  10, "daily", "high"))
    pet.addTask(Task("Medium task", 30, "daily", "high"))
    owner.addPet(pet)

    scheduler = Scheduler(owner)
    scheduler.generatePlan()

    sorted_tasks = scheduler.sortByDuration()
    durations = [t.duration for t in sorted_tasks]
    assert durations == sorted(durations), "Tasks are not sorted ascending by duration"


def test_sort_by_duration_does_not_mutate_schedule():
    """sortByDuration() should not change the internal schedule order."""
    owner = Owner("Alex", available_time=120)
    pet = Pet("Buddy", "dog")
    pet.addTask(Task("High priority short", 10, "daily", "high"))
    pet.addTask(Task("High priority long",  60, "daily", "high"))
    owner.addPet(pet)

    scheduler = Scheduler(owner)
    scheduler.generatePlan()

    original_order = [t.description for t in scheduler.getSchedule()]
    scheduler.sortByDuration()   # call it
    after_order = [t.description for t in scheduler.getSchedule()]

    assert original_order == after_order, "sortByDuration() mutated the internal schedule"


# ── Recurrence logic ──────────────────────────────────────────────────────────

def test_daily_task_next_due_is_tomorrow():
    """markComplete() on a daily task should set next_due to tomorrow."""
    task = Task("Walk", 30, "daily", "high")
    task.markComplete()
    assert task.next_due == date.today() + timedelta(days=1)


def test_weekly_task_next_due_is_seven_days():
    """markComplete() on a weekly task should set next_due to 7 days from today."""
    task = Task("Flea meds", 10, "weekly", "medium")
    task.markComplete()
    assert task.next_due == date.today() + timedelta(weeks=1)


def test_as_needed_task_next_due_is_none():
    """markComplete() on an as-needed task should leave next_due as None."""
    task = Task("Vet visit", 45, "as-needed", "high")
    task.markComplete()
    assert task.next_due is None


def test_is_due_today_false_after_completion():
    """A completed daily task should not be isDueToday() until tomorrow."""
    task = Task("Walk", 30, "daily", "high")
    task.markComplete()
    # next_due is tomorrow, so isDueToday should be False
    assert task.isDueToday() is False


def test_is_due_today_true_before_completion():
    """A fresh task with no next_due should always be isDueToday()."""
    task = Task("Feed", 10, "daily", "high")
    assert task.isDueToday() is True


# ── Edge cases ────────────────────────────────────────────────────────────────

def test_pet_with_no_tasks_produces_empty_schedule():
    """A pet with zero tasks should result in an empty schedule."""
    owner = Owner("Alex", available_time=90)
    owner.addPet(Pet("Buddy", "dog"))   # no tasks added

    scheduler = Scheduler(owner)
    scheduler.generatePlan()

    assert scheduler.getSchedule() == []
    assert "0 task(s)" in scheduler.getSummary()


def test_owner_with_no_pets_produces_empty_schedule():
    """An owner with no pets registered should produce an empty schedule."""
    owner = Owner("Alex", available_time=90)
    scheduler = Scheduler(owner)
    scheduler.generatePlan()
    assert scheduler.getSchedule() == []


def test_tasks_exceeding_budget_are_excluded():
    """Tasks that push total duration over available_time should be excluded."""
    owner = Owner("Alex", available_time=20)
    pet = Pet("Buddy", "dog")
    pet.addTask(Task("Walk", 15, "daily", "high"))
    pet.addTask(Task("Bath", 15, "daily", "medium"))   # won't fit — only 5 min left
    owner.addPet(pet)

    scheduler = Scheduler(owner)
    scheduler.generatePlan()

    scheduled_descriptions = [t.description for t in scheduler.getSchedule()]
    assert "Walk" in scheduled_descriptions
    assert "Bath" not in scheduled_descriptions


# ── Conflict detection ────────────────────────────────────────────────────────

def test_no_conflicts_when_tasks_fit_sequentially():
    """A normal schedule with one task per pet should have no conflicts."""
    owner = Owner("Alex", available_time=60)
    pet = Pet("Buddy", "dog")
    pet.addTask(Task("Walk", 30, "daily", "high"))
    owner.addPet(pet)

    scheduler = Scheduler(owner)
    scheduler.generatePlan()

    assert scheduler.detectConflicts() == []


def test_filter_by_pet_returns_correct_tasks():
    """filterByPet() should return only that pet's tasks."""
    owner = Owner("Alex", available_time=120)
    buddy = Pet("Buddy", "dog")
    luna  = Pet("Luna",  "cat")
    buddy.addTask(Task("Walk", 30, "daily", "high"))
    luna.addTask(Task("Feed", 10, "daily", "high"))
    owner.addPet(buddy)
    owner.addPet(luna)

    scheduler = Scheduler(owner)
    scheduler.generatePlan()

    luna_tasks = scheduler.filterByPet("luna")
    assert len(luna_tasks) == 1
    assert luna_tasks[0].description == "Feed"


def test_filter_by_status_pending():
    """filterByStatus(False) should return only incomplete tasks."""
    owner = Owner("Alex", available_time=120)
    pet = Pet("Buddy", "dog")
    t1 = Task("Walk", 30, "daily", "high")
    t2 = Task("Feed", 10, "daily", "high")
    pet.addTask(t1)
    pet.addTask(t2)
    owner.addPet(pet)

    t1.markComplete()

    scheduler = Scheduler(owner)
    scheduler.generatePlan()

    pending = scheduler.filterByStatus(completed=False)
    assert all(not t.isCompleted for t in pending)
    assert t2 in pending
    assert t1 not in pending
