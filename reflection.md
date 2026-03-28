# PawPal+ Project Reflection

## 1. System Design
- add/remove a pet
- add/remove daily & weekly tasks
- check tasks as completed

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

classes: Task, Pet & Scheduler
responsibilities:
1) Task: Store tasks for each pet (task name, frequency, due date, description), complete tasks as marked.
2) Pet: store list of pets (pet name, species, age, associated task).
3) Scheduler: add/remove pets, view all tasks for each pet, see upcoming and completed tasks, check conficts, generate recurring tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

I made several changes based on AI feedback on missing relationships or potential logic bottlenecks. For example:
    1.	Added remove_pet & remove_task method on Task & Scheduler. Even though my initial design had these, the AI generated skeleton missed on including the methods. 
    2.	Added pet param to check_conflict to relate which pet the task belongs to.


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
