import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


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
