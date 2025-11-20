# Architecture Documentation

## System Overview
The Personal Study Planner AI Agent is a multi-agent system designed to assist students in managing their study schedules. It uses a hub-and-spoke architecture where the **Orchestrator Agent** coordinates communication between specialized agents.

## Agents

### 1. Orchestrator Agent
- **Role:** Central coordinator.
- **Responsibilities:** Receives user input, determines intent, and delegates tasks to appropriate agents.

### 2. Scheduler Agent
- **Role:** Schedule creator.
- **Responsibilities:** Generates initial study plans based on course load, difficulty, and user preferences.

### 3. Reschedule Agent
- **Role:** Schedule adjuster.
- **Responsibilities:** Handles modifications to the schedule due to missed sessions or new conflicts.

### 4. Progress Tracker Agent
- **Role:** Performance monitor.
- **Responsibilities:** Tracks completed sessions, calculates completion rates, and identifies weak areas.

### 5. Reminder Agent
- **Role:** Notifier.
- **Responsibilities:** Sends scheduled reminders and motivational messages.

### 6. Context Manager Agent
- **Role:** State manager.
- **Responsibilities:** Persists user profiles, preferences, and session history.

## Data Flow
1. **User Input:** User interacts via CLI/Web.
2. **Orchestration:** Orchestrator analyzes input.
3. **Delegation:** Orchestrator calls specific agent (e.g., Scheduler).
4. **Execution:** Agent performs task using Tools (e.g., `calculate_study_hours`).
5. **Persistence:** Context Manager saves/loads state from JSON files.
6. **Response:** Agent returns result to Orchestrator, which formats response for user.

## Data Storage
- **Users:** `data/users/{user_id}.json`
- **Schedules:** `data/schedules/{user_id}_schedule.json`
