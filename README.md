# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Features

### Core scheduling
- **Priority-based daily plan** — tasks are sorted high → medium → low and greedily fit into the owner's time budget
- **Per-decision reasoning** — every INCLUDED / EXCLUDED decision is explained with how much time remained

### Smarter scheduling (Phase 3)
- **Sort by duration** — view the scheduled plan reordered shortest-to-longest to front-load quick wins
- **Filter by pet** — isolate the schedule for a single pet
- **Filter by completion status** — see pending vs. completed tasks across all pets
- **Recurring task automation** — `markComplete()` automatically calculates the next due date using `timedelta` (daily → tomorrow, weekly → +7 days)
- **Conflict detection** — the Scheduler checks for overlapping time slots per pet and surfaces warning banners in the UI before the owner acts on the plan

### UI
- Streamlit app with persistent session state — data survives every button click
- Color-coded priority badges (🔴 high / 🟡 medium / 🟢 low)
- Skipped tasks panel showing what didn't fit and why
- Conflict warnings rendered as `st.error` / `st.warning` banners so they're impossible to miss

---

## 📸 Demo

<a href="/Users/imran/Desktop/codepath/ai110-pawpal/ai110-module2show-pawpal-starter/Screenshot 2026-03-29 at 11.47.16 PM.png" target="_blank"><img src='/Users/imran/Desktop/codepath/ai110-pawpal/ai110-module2show-pawpal-starter/Screenshot 2026-03-29 at 11.47.16 PM.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

---

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Testing PawPal+

Run the full test suite:

```bash
python -m pytest tests/ -v
```

**Coverage (15 tests):**

| Area | Tests |
|---|---|
| Task basics | completion flag, task addition to pet |
| Sorting | ascending duration order, schedule not mutated |
| Recurrence | daily → tomorrow, weekly → +7 days, as-needed → None, `isDueToday()` before/after |
| Edge cases | pet with no tasks, owner with no pets, tasks exceeding budget are excluded |
| Conflict detection | no false positives on clean schedule |
| Filtering | `filterByPet()` by name, `filterByStatus()` for pending tasks |

**Confidence level: ★★★★☆**
Core scheduling, sorting, recurrence, and filtering are fully verified. The conflict detection uses a simplified sequential-offset model (see `reflection.md` section 2b) which can produce false positives in real-world multi-pet scenarios — that edge case is not yet covered by automated tests.

---

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
