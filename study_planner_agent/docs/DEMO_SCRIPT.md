# Demo Script Walkthrough

## Running the Demo
To execute the full demo scenario, run:
```bash
python study_planner_agent/demo_script.py
```

## Scenario Overview
The demo simulates a student ("demo_user") interacting with the agent to prepare for exams in late December 2025.

### Act 1: Schedule Creation
*   **User**: Requests a study plan.
*   **System**: Loads the demo profile (5 subjects, specific exam dates).
*   **Scheduler**: Generates a plan respecting the 5-hour daily limit and morning preference.
*   **Output**: Shows a preview of the first week's schedule.

### Act 2: Progress Update
*   **User**: Asks for a status report.
*   **Progress Agent**: Displays an ASCII bar chart showing completion rates for each subject.

### Act 3: Handling Missed Sessions
*   **User**: Reports a missed "Discrete Math" session.
*   **Rescheduler**: Acknowledges the miss and proposes a makeup slot on the next available Saturday.

### Act 4: Motivation
*   **User**: Expresses feeling overwhelmed.
*   **Reminder Agent**: Sends an encouraging message displayed in a formatted box.

## Key Verification Points
*   Verify that exam dates are respected (Revision/Mock tests scheduled correctly).
*   Check that study hours are distributed based on difficulty (High difficulty subjects get more time).
*   Ensure the makeup slot logic finds a valid future time.
