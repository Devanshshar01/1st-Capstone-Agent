import pytest
import datetime
from tools.scheduler_tools import calculate_study_hours, optimize_time_slots, generate_weekly_plan

def test_calculate_study_hours():
    courses_data = {
        "Math": {
            "topics": ["Algebra", "Calculus"],
            "difficulty": "high",
            "current_progress": 0.0
        }
    }
    exam_dates = {"Math": (datetime.date.today() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")}
    available_hours = 4
    
    result = calculate_study_hours(courses_data, exam_dates, available_hours)
    
    assert "Math" in result
    # 2 topics * 1.5 (high) = 3.0 hours total
    assert result["Math"]["total_hours"] == 3.0
    assert len(result["Math"]["topics_distribution"]) == 2

def test_generate_weekly_plan():
    courses_data = {
        "Physics": {
            "topics": ["Mechanics", "Optics"],
            "difficulty": "medium", # 1.0 mult
            "current_progress": 0.0
        }
    }
    # Exam in 10 days
    exam_date = (datetime.date.today() + datetime.timedelta(days=10)).strftime("%Y-%m-%d")
    exam_dates = {"Physics": exam_date}
    
    user_prefs = {
        "preferred_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "session_duration": 1,
        "peak_hours": "morning"
    }
    
    start_date = datetime.date.today().strftime("%Y-%m-%d")
    
    plan = generate_weekly_plan(courses_data, exam_dates, user_prefs, start_date)
    
    assert "daily_schedule" in plan
    assert "course_analysis" in plan
    assert plan["course_analysis"]["Physics"]["total_hours"] == 2.0 # 2 topics * 1.0
