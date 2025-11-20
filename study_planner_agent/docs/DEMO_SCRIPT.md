# Demo Script

## Scenario: New Student Setup and Rescheduling

### Step 1: Initialization
- Run `python data/demo_data.py` to create the "student_01" profile.
- Run `python app.py` to start the agent.

### Step 2: Interaction
**User:** "Create a study plan for me."
**Agent:** (Orchestrator delegates to Scheduler) "Creating schedule for user student_01..."

**User:** "I missed my session yesterday."
**Agent:** (Orchestrator delegates to Rescheduler) "Rescheduling session..."

**User:** "How am I doing?"
**Agent:** (Orchestrator delegates to Progress) "Progress Report: On Track"

### Step 3: Verification
- Check `data/users/student_01.json` for updates.
- Check logs in `agent.log` for internal trace.
