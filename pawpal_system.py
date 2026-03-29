from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Pet:
    name: str
    vitals: dict = field(default_factory=lambda: {"hunger": 0, "sleep": 0, "hydration": 0})
    care: dict = field(default_factory=lambda: {"walking": False, "grooming": False, "medication": False})
    owner: Optional["User"] = field(default=None, repr=False)

    def getVitals(self) -> dict:
        return self.vitals

    def setVitals(self, key: str, value) -> None:
        self.vitals[key] = value

    def getCare(self) -> dict:
        return self.care

    def setCare(self, key: str, value) -> None:
        self.care[key] = value


@dataclass
class Task:
    name: str
    duration: int  # in minutes
    priority: str  # "high", "medium", "low"
    category: str  # "walk", "feed", "meds", "groom", "enrichment"
    pet: Optional[Pet] = None
    isCompleted: bool = False

    def getDuration(self) -> int:
        return self.duration

    def getPriority(self) -> str:
        return self.priority

    def getCategory(self) -> str:
        return self.category

    def markComplete(self) -> None:
        self.isCompleted = True


class Constraints:
    def __init__(self, available_time: int, preferred_time_slots: list = None, blocked_times: list = None):
        self.availableTime = available_time
        self.preferredTimeSlots = preferred_time_slots or []
        self.blockedTimes = blocked_times or []

    def getAvailableTime(self) -> int:
        return self.availableTime

    def isTimeAvailable(self, slot: str) -> bool:
        return slot not in self.blockedTimes


class User:
    def __init__(self, name: str, username: str):
        self.name = name
        self.username = username
        self.petList: list[Pet] = []
        self.userConstraints: Optional[Constraints] = None

    def getName(self) -> str:
        return self.name

    def setName(self, name: str) -> None:
        self.name = name

    def getUsername(self) -> str:
        return self.username

    def setUsername(self, username: str) -> None:
        self.username = username

    def adoptPet(self, pet: Pet) -> None:
        pet.owner = self
        self.petList.append(pet)


class Plan:
    def __init__(self, owner: User, date: str):
        self.owner = owner
        self.date = date
        self.scheduledTasks: list[Task] = []
        self.totalDuration: int = 0
        self.reasoning: str = ""

    def generatePlan(self, tasks: list[Task], constraints: Constraints) -> None:
        pass  # TODO: implement scheduling logic

    def addTask(self, task: Task) -> None:
        self.scheduledTasks.append(task)
        self.totalDuration += task.duration

    def removeTask(self, task: Task) -> None:
        if task in self.scheduledTasks:
            self.scheduledTasks.remove(task)
            self.totalDuration -= task.duration

    def getReasoning(self) -> str:
        return self.reasoning

    def displayPlan(self) -> None:
        pass  # TODO: implement display logic
