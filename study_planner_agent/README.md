# Personal Study Planner AI Agent

A multi-agent system designed to help students manage their study schedules, track progress, and stay motivated.

## Features
*   **Advanced Scheduling**: Dynamic time allocation based on difficulty and exam dates.
*   **Rescheduling**: Smart handling of missed sessions.
*   **Progress Tracking**: Visual reports and weak area identification.
*   **Motivation**: Personalized reminders and encouragement.
*   **CLI Interface**: Interactive wizard for creating schedules.

## Installation
1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Configure environment:
    *   Copy `.env.example` to `.env`
    *   Add your `GOOGLE_API_KEY`

## Usage
Run the application in CLI mode:
```bash
python app.py
```

### Commands
*   `/schedule`: Create a new study plan.
*   `/progress`: View progress report.
*   `/help`: Show available commands.

## Demo
To run a full walkthrough scenario:
```bash
python demo_script.py
```

## Architecture
See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design details.
