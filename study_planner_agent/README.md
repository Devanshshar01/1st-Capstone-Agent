# Personal Study Planner AI Agent

## Overview
The Personal Study Planner AI Agent is a multi-agent system designed to help college students create optimized study schedules, track their progress, and stay motivated. It leverages Google's Gemini models to orchestrate various agents for scheduling, rescheduling, progress tracking, and context management.

## Problem Statement
Students often struggle with time management, balancing multiple courses, and adapting to unexpected changes in their schedule. This agent aims to solve these problems by providing a dynamic and personalized study planning assistant.

## Features
- **Smart Scheduling:** Generates optimized study plans based on course load and deadlines.
- **Dynamic Rescheduling:** Automatically adjusts plans when sessions are missed.
- **Progress Tracking:** Monitors performance and identifies weak areas.
- **Context Awareness:** Remembers user preferences and past performance.
- **Motivational Reminders:** Sends timely notifications to keep students on track.

## Architecture
The system consists of the following agents:
1. **Orchestrator Agent:** Coordinates all other agents.
2. **Scheduler Agent:** Creates the initial study plan.
3. **Reschedule Agent:** Handles modifications to the plan.
4. **Progress Tracker Agent:** Analyzes user performance.
5. **Reminder Agent:** Manages notifications.
6. **Context Manager Agent:** Maintains user state and memory.

## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your `GOOGLE_API_KEY`

## Usage
Run the main application:
```bash
python app.py
```

## Demo
(Link to demo video or script)

## Tech Stack
- **AI Model:** Google Gemini (via `google-generativeai`)
- **Language:** Python 3.10+
- **Data Storage:** JSON (File-based persistence)
- **Testing:** Pytest

## Kaggle Capstone Submission
This project is submitted for the Kaggle Agents Intensive Capstone.

## Future Enhancements
- Integration with Google Calendar.
- Mobile app interface.
- Advanced analytics dashboard.
