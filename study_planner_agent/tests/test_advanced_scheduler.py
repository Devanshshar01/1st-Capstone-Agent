import pytest
import datetime
from tools.scheduler_tools import calculate_study_hours, optimize_time_slots, generate_weekly_plan

def test_calculate_study_hours():
    courses_data = {
        "Math": {
            "topics": ["Algebra", "Calculus"],
            "difficulty": "high",
            "current_progress": 0.0,
            "exam_date": (datetime.date.today() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        }
    }
    exam_dates = {"Math": courses_data["Math"]["exam_date"]}
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
            "current_progress": 0.0,
            "exam_date": (datetime.date.today() + datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        }
    }
    # Exam in 10 days
    exam_dates = {"Physics": courses_data["Physics"]["exam_date"]}
    
    user_prefs = {
        "preferred_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "session_duration": 1,
        "peak_hours": "morning",
        "available_hours_per_day": 4
    }
    
    start_date = datetime.date.today().strftime("%Y-%m-%d")
    
    plan = generate_weekly_plan(courses_data, exam_dates, user_prefs, start_date)
    
    assert "daily_schedule" in plan
    assert "course_analysis" in plan
    assert plan["course_analysis"]["Physics"]["total_hours"] == 2.0 # 2 topics * 1.0

def test_custom_user_constraints():
    """
    Test that the scheduler respects user-defined constraints like available hours and peak times.
    """
    courses_data = {
        "History": {
            "topics": ["Ancient", "Medieval", "Modern"],
            "difficulty": "medium",
            "current_progress": 0.0,
            "exam_date": (datetime.date.today() + datetime.timedelta(days=15)).strftime("%Y-%m-%d")
        }
    }
    exam_dates = {"History": courses_data["History"]["exam_date"]}
    
    # Case 1: Limited hours (should scale down or fit tightly)
    user_prefs_limited = {
        "preferred_days": ["Saturday", "Sunday"],
        "session_duration": 1,
        "peak_hours": "evening",
        "available_hours_per_day": 1 # Very limited
    }
    
    start_date = datetime.date.today().strftime("%Y-%m-%d")
    plan = generate_weekly_plan(courses_data, exam_dates, user_prefs_limited, start_date)
    
    # Check that sessions are scheduled in the evening (after 18:00)
    schedule = plan["daily_schedule"]
    for date, sessions in schedule.items():
        for session in sessions:
            start_hour = int(session["start_time"].split(":")[0])
            assert start_hour >= 18, f"Session scheduled at {start_hour}, expected >= 18 for evening peak"

    # Case 2: User defined subjects/topics are preserved
    assert "History" in plan["course_analysis"]
    assert "Ancient" in plan["course_analysis"]["History"]["topics_distribution"]
