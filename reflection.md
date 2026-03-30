# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- These are the classes that can be indentify: User, Pet, Task, Constraints, Plan
- For the class User these are the attributes: Name, Username, PetList (objects of pet class), UserConstraints (objects of constraints class); methods: getName, setName, getUsername, setUsername, adoptPet, 
- For the class Pet these are the attributes: Name, Owner (an object of user class), Vitals ( a dictionary with hunger, sleep, hydration as dictioanry keys), Care ( a dictionary with walking, grooming, medication as dictionary keys); methods: getVitals, getCare, setVitals, setCare
- For the class Task the attributes are name, duration, priority, category, pet (an object from Pet class); method: isCompleted, getDuration, getPriority, getCategory, markComplete.
- For the class Constraints the attributes are availableTime, preferredTimeSlots, blockedTimes; method: grtAvailableTime, isTimeAvailable.
- For the class Plan the attributes are owner ( an object with User class), date, scheduledTasks ( an object from Task class), totalDuration, reasoning; method: generatePlan, addTask, removeTask, getReasoning, displayPlan.

**Final UML (updated to match implementation):**

   classDiagram
    class User {
        +String name
        +String username
        +List~Pet~ petList
        +Constraints userConstraints
        +getName() String
        +setName(name) void
        +getUsername() String
        +setUsername(username) void
        +adoptPet(pet) void
    }

    class Pet {
        +String name
        +User owner
        +Dict vitals
        +Dict care
        +getVitals() Dict
        +setVitals(key, value) void
        +getCare() Dict
        +setCare(key, value) void
    }

    class Task {
        +String description
        +int duration
        +String frequency
        +String priority
        +bool isCompleted
        +date next_due
        +markComplete() void
        +reset() void
        +isDue() bool
        +isDueToday() bool
        +getDuration() int
        +getPriority() String
    }

    class Owner {
        +String name
        +int available_time
        -List~Pet~ _pets
        +addPet(pet) void
        +getPets() List
        +getAllTasks() List
    }

    class Scheduler {
        +Owner owner
        -List _schedule
        -List _excluded
        -String _reasoning
        -String _summary
        +generatePlan() void
        +getSchedule() List
        +getReasoning() String
        +getSummary() String
        +sortByDuration() List
        +filterByStatus(completed) List
        +filterByPet(pet_name) List
        +detectConflicts() List
    }

    Owner "1" --> "many" Pet : owns
    Pet "1" --> "many" Task : has
    Scheduler "1" --> "1" Owner : plans for
    Scheduler "1" --> "many" Task : schedules

**b. Design changes**

- During implementation, my design changed in a few key ways.

Initially, I designed separate classes like Constraints and Plan to handle scheduling logic and user preferences. However, as I began implementing the system, I realized this added unnecessary complexity for a CLI-first version of the app.

I refactored the design by introducing a Scheduler class that centralizes task organization, sorting, filtering, and conflict detection. This reduced the need for a separate Plan class and simplified how components interact.

I also replaced the original User class with an Owner class that directly manages pets and tasks. This made the relationships between objects clearer and more aligned with the system’s core functionality.

These changes improved modularity and made the system easier to test and extend.

- The scheduler considers several constraints when generating a plan:

- Available time of the owner
- Task duration
- Task priority
- Task frequency (daily, weekly)
- Completion status

Among these, priority and available time were the most important. Tasks with higher priority are scheduled first, and the system ensures that the total scheduled time does not exceed the owner’s available time.

I chose this approach because it reflects real-world decision-making, where urgent tasks must be completed within limited time.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

The conflict-detection algorithm assigns each scheduled task a time slot by accumulating start offsets in the order tasks appear in `_schedule` (sorted by priority). Two tasks for the same pet are placed back-to-back on a single shared timeline rather than being given independent parallel windows.

The tradeoff is **realism vs. simplicity**. In a real calendar a pet owner might walk Buddy at 8 AM and give flea medication at 9 AM — two events that never truly overlap. The sequential-offset model has no concept of clock time, so it can report an overlap whenever two same-pet tasks share any portion of that artificial timeline, producing false-positive warnings in realistic usage.

This tradeoff is still reasonable because: (1) it requires no external calendar dependency, (2) it catches the genuinely problematic case where two tasks for the same pet are double-booked beyond the owner's time budget, and (3) the public API of `detectConflicts()` can be upgraded to real datetime slot assignment later without breaking callers.

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI (Claude Code) throughout different phases of the project:

- During design, I used AI to brainstorm class structures and relationships.
- During implementation, AI helped generate method skeletons and suggest logic for sorting and filtering tasks.
- During testing, AI assisted in creating initial pytest test cases and explaining failures.

The most helpful prompts were specific and contextual, such as:
"How should the Scheduler retrieve tasks from multiple pets?"
"How can I sort tasks by time using Python?"
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- One moment where I did not accept an AI suggestion was when it proposed combining multiple responsibilities into a single method inside the Scheduler.

Although the suggestion worked functionally, it reduced readability and violated separation of concerns. I chose to split the logic into smaller, focused methods instead.

To verify AI-generated code, I:
- Ran my CLI demo (main.py)
- Wrote and executed pytest tests
- Manually reviewed edge cases (e.g., empty task lists, duplicate times)

This ensured that the system behaved correctly and aligned with my design goals.

---

## 4. Testing and Verification

**a. What you tested**

- I tested several core behaviors of the system:

- Task completion updates the status correctly
- Adding tasks to a pet increases the task count
- Sorting returns tasks in the correct order
- Conflict detection flags duplicate task times

These tests were important because they validate the core functionality of the scheduler and ensure that the system behaves predictably.

**b. Confidence**

- I am moderately confident (4/5) that my scheduler works correctly for the intended use cases.

- If I had more time, I would test additional edge cases such as:
- Tasks with overlapping durations instead of exact matches
- Pets with no tasks
- Extremely large numbers of tasks
- Invalid or missing input data

These tests would improve robustness and reliability.

---

## 5. Reflection

**a. What went well**

- The part I am most satisfied with is the modular design of the system.

Separating responsibilities across classes like Owner, Pet, Task, and Scheduler made the system easier to understand and extend. The Scheduler acting as the "brain" of the system worked especially well.

**b. What you would improve**

- If I had another iteration, I would improve the time handling system.

Currently, the scheduler uses a simplified timeline model instead of real datetime objects. I would redesign this to support actual time slots and overlapping durations for more realistic scheduling. As right now, it looks like a simple timetable

**c. Key takeaway**

- One important thing I learned is that AI is a powerful assistant, but I must act as the lead architect.

AI can generate code quickly, but it does not always produce the best design. I learned to evaluate, refine, and sometimes reject AI suggestions to maintain a clean and scalable system.

This project helped me understand how to balance speed (AI assistance) with thoughtful engineering decisions.
