import pytest
from agents.orchestrator import OrchestratorAgent
from agents.scheduler_agent import SchedulerAgent
from tools.scheduler_tools import calculate_study_hours

def test_orchestrator_initialization():
    orchestrator = OrchestratorAgent()
    assert orchestrator.agents == {}

def test_orchestrator_registration():
    orchestrator = OrchestratorAgent()
    scheduler = SchedulerAgent()
    orchestrator.register_agent("scheduler", scheduler)
    assert "scheduler" in orchestrator.agents
    assert orchestrator.agents["scheduler"] == scheduler

def test_calculate_study_hours():
    courses = [
        {"difficulty": 2, "credits": 3}, # 6 hours
        {"difficulty": 3, "credits": 4}  # 12 hours
    ]
    total = calculate_study_hours(courses)
    assert total == 18
