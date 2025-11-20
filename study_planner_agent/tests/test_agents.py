import pytest
import datetime
from agents.scheduler_agent import SchedulerAgent
from agents.reschedule_agent import RescheduleAgent
from agents.progress_agent import ProgressAgent
from agents.reminder_agent import ReminderAgent
from agents.orchestrator import OrchestratorAgent

# Mock Data
MOCK_COURSES = {
    "Math": {
        "topics": ["Algebra", "Calculus"],
        "difficulty": "high",
        "exam_date": "2025-12-20"
    }
}

MOCK_PREFS = {
    "daily_max_hours": 5,
    "peak_hours": "morning",
    "session_duration": 2
}

@pytest.fixture
def orchestrator():
    orch = OrchestratorAgent()
    orch.register_agent("scheduler", SchedulerAgent())
    orch.register_agent("rescheduler", RescheduleAgent())
    orch.register_agent("progress", ProgressAgent())
    orch.register_agent("reminder", ReminderAgent())
    return orch

def test_scheduler_agent_creation(orchestrator):
    result = orchestrator.agents["scheduler"].create_schedule("test_user", MOCK_COURSES, MOCK_PREFS)
    assert result["status"] == "success"
    assert "daily_schedule" in result["schedule"]
    
    # Verify exam prep
    schedule = result["schedule"]["daily_schedule"]
    # Mock test on 19th
    assert "2025-12-19" in schedule
    assert any(s["topic"] == "FULL MOCK TEST" for s in schedule["2025-12-19"])
    # Revision on 18th
    assert "2025-12-18" in schedule
    assert any(s["topic"] == "FINAL REVISION" for s in schedule["2025-12-18"])

def test_reschedule_agent_conflict(orchestrator):
    missed = [{"subject": "Math", "topic": "Algebra", "date": "2025-11-22"}]
    response = orchestrator.agents["rescheduler"].handle_missed_session("test_user", missed)
    assert response["status"] == "success"
    assert len(response["proposed_alternatives"]) > 0
    assert response["proposed_alternatives"][0]["suggested_slot"]["type"] == "makeup"

def test_progress_agent_metrics(orchestrator):
    metrics = orchestrator.agents["progress"].get_insights("test_user")
    assert "weak_areas" in metrics
    assert "metrics" in metrics

def test_orchestrator_routing(orchestrator):
    response = orchestrator.process_request("Show my progress", "test_user")
    assert "Progress Report" in response
    
    response = orchestrator.process_request("Motivate me", "test_user")
    assert "Motivation sent" in response
