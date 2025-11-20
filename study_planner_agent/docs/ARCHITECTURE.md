# Architecture Documentation

## Overview
The **Personal Study Planner AI Agent** is a multi-agent system designed to help students manage their study schedules, track progress, and stay motivated. It uses a modular architecture where specialized agents handle specific responsibilities.

## Core Components

### 1. Agents
*   **OrchestratorAgent**: The central hub that routes user requests to the appropriate sub-agent.
*   **SchedulerAgent**: Generates optimized study plans using custom algorithms (`calculate_study_hours`, `optimize_time_slots`).
*   **RescheduleAgent**: Handles missed sessions and conflicts, proposing alternative slots.
*   **ProgressAgent**: Tracks completion rates and provides analytical reports.
*   **ReminderAgent**: Manages notifications and sends motivational messages.
*   **ContextAgent**: Manages persistent state (user profiles, preferences) and memory.

### 2. Tools
*   **Scheduler Tools**: `calculate_study_hours`, `optimize_time_slots`, `generate_weekly_plan`.
*   **Reschedule Tools**: `detect_conflicts`, `find_alternative_slots`, `rebalance_schedule`.
*   **Progress Tools**: `track_session_completion`, `calculate_progress_metrics`.
*   **Notification Tools**: `schedule_reminder`, `send_notification` (ASCII art).
*   **Memory Tools**: `save_user_profile`, `load_user_profile`.

### 3. Data Layer
*   **File System Storage**: JSON files stored in `data/users/` for user profiles and schedules.
*   **Configuration**: `config.py` and `.env` for environment variables and constants.

## Data Flow
1.  **User Input**: CLI or Web Interface receives command.
2.  **Orchestration**: `OrchestratorAgent` analyzes intent.
3.  **Execution**: Specialized agent calls relevant tools.
4.  **Persistence**: `ContextAgent` saves state to disk.
5.  **Response**: Agent returns formatted response to user.

## Directory Structure
```
study_planner_agent/
├── agents/         # Agent classes
├── tools/          # Functional logic
├── data/           # JSON storage
├── utils/          # Helpers
├── docs/           # Documentation
├── tests/          # Unit tests
├── app.py          # Entry point
└── config.py       # Configuration
```
