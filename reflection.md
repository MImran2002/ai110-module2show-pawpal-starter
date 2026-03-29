# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- These are the classes that can be indentify: User, Pet, Task, Constraints, Plan
- For the class User these are the attributes: Name, Username, PetList (objects of pet class), UserConstraints (objects of constraints class); methods: getName, setName, getUsername, setUsername, adoptPet, 
- For the class Pet these are the attributes: Name, Owner (an object of user class), Vitals ( a dictionary with hunger, sleep, hydration as dictioanry keys), Care ( a dictionary with walking, grooming, medication as dictionary keys); methods: getVitals, getCare, setVitals, setCare
- For the class Task the attributes are name, duration, priority, category, pet (an object from Pet class); method: isCompleted, getDuration, getPriority, getCategory, markComplete.
- For the class Constraints the attributes are availableTime, preferredTimeSlots, blockedTimes; method: grtAvailableTime, isTimeAvailable.
- For the class Plan the attributes are owner ( an object with User class), date, scheduledTasks ( an object from Task class), totalDuration, reasoning; method: generatePlan, addTask, removeTask, getReasoning, displayPlan.

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
        +String name
        +int duration
        +String priority
        +String category
        +Pet pet
        +bool isCompleted
        +getDuration() int
        +getPriority() String
        +getCategory() String
        +markComplete() void
    }

    class Constraints {
        +int availableTime
        +List preferredTimeSlots
        +List blockedTimes
        +getAvailableTime() int
        +isTimeAvailable(slot) bool
    }

    class Plan {
        +User owner
        +String date
        +List~Task~ scheduledTasks
        +int totalDuration
        +String reasoning
        +generatePlan(tasks, constraints) void
        +addTask(task) void
        +removeTask(task) void
        +getReasoning() String
        +displayPlan() void
    }

    User "1" --> "many" Pet : owns
    User "1" --> "1" Constraints : has
    Pet "1" --> "many" Task : has
    Plan "1" --> "1" User : belongs to
    Plan "1" --> "many" Task : schedules 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
