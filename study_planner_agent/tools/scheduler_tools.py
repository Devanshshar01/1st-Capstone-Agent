import datetime
import math
from typing import List, Dict, Any, Optional

def calculate_study_hours(courses_data: Dict[str, Any], exam_dates: Dict[str, str], available_hours_per_day: int) -> Dict[str, Any]:
    """
    Calculates optimal study time distribution based on syllabus and exam schedule.
    """
    schedule_data = {}
    today = datetime.date.today()
    
    # Difficulty multipliers
    difficulty_mult = {"high": 1.5, "medium": 1.0, "low": 0.7}
    
    for course_name, data in courses_data.items():
        exam_date_str = exam_dates.get(course_name)
        if not exam_date_str:
            continue
            
        exam_date = datetime.datetime.strptime(exam_date_str, "%Y-%m-%d").date()
        days_until_exam = (exam_date - today).days
        
        # Reserve 2 days for revision
        study_days = max(0, days_until_exam - 2)
        if study_days == 0:
            continue

        # Calculate base hours needed
        num_topics = len(data.get("topics", []))
        difficulty = data.get("difficulty", "medium").lower()
        multiplier = difficulty_mult.get(difficulty, 1.0)
        
        total_hours_needed = num_topics * multiplier
        
        # Adjust for progress
        progress = data.get("current_progress", 0.0)
        total_hours_needed *= (1.0 - progress)
        
        # Cap daily hours if needed (simple distribution for now)
        # This is a simplified logic; real logic would balance across all courses
        # Here we just calculate what is needed per course
        
        weeks_until_exam = math.ceil(study_days / 7)
        hours_per_week = []
        
        if weeks_until_exam > 0:
            avg_hours_per_week = total_hours_needed / weeks_until_exam
            hours_per_week = [round(avg_hours_per_week, 1)] * weeks_until_exam
        
        # Distribute hours among topics
        topics_dist = {}
        if num_topics > 0:
            hours_per_topic = total_hours_needed / num_topics
            for topic in data.get("topics", []):
                topics_dist[topic] = round(hours_per_topic, 1)
                
        schedule_data[course_name] = {
            "total_hours": round(total_hours_needed, 1),
            "hours_per_week": hours_per_week,
            "topics_distribution": topics_dist,
            "exam_date": exam_date_str
        }
        
    return schedule_data

def optimize_time_slots(course_schedule: Dict[str, Any], user_preferences: Dict[str, Any], start_date: datetime.date) -> Dict[str, List[Dict[str, Any]]]:
    """
    Generates specific time slots for study sessions.
    """
    daily_schedule = {}
    current_date = start_date
    
    preferred_days = user_preferences.get("preferred_days", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    session_duration = user_preferences.get("session_duration", 2) # hours
    start_hour_pref = 9 # Default start at 9 AM
    
    if user_preferences.get("peak_hours") == "morning":
        start_hour_pref = 8
    elif user_preferences.get("peak_hours") == "afternoon":
        start_hour_pref = 14
    elif user_preferences.get("peak_hours") == "evening":
        start_hour_pref = 18
        
    # Flatten the weekly requirements into a queue of sessions
    # This is a simplified greedy allocation
    
    # We'll plan for 4 weeks max for this demo or until exams
    for week_num in range(4):
        # Gather weekly tasks
        weekly_tasks = []
        for course, data in course_schedule.items():
            hours_list = data.get("hours_per_week", [])
            if week_num < len(hours_list):
                hours = hours_list[week_num]
                # Create sessions
                num_sessions = math.ceil(hours / session_duration)
                topics = list(data.get("topics_distribution", {}).keys())
                
                for i in range(num_sessions):
                    topic = topics[i % len(topics)] if topics else "General Study"
                    weekly_tasks.append({
                        "subject": course,
                        "topic": topic,
                        "duration": session_duration
                    })
        
        # Distribute weekly tasks across preferred days
        # Simple round-robin for now
        days_in_week = []
        for i in range(7):
            day_date = current_date + datetime.timedelta(days=i)
            if day_date.strftime("%A") in preferred_days:
                days_in_week.append(day_date)
        
        task_idx = 0
        for day_date in days_in_week:
            date_str = day_date.isoformat()
            daily_schedule[date_str] = []
            
            current_time = datetime.datetime.combine(day_date, datetime.time(start_hour_pref, 0))
            
            # Try to fit up to 2 sessions per day
            sessions_today = 0
            while sessions_today < 2 and task_idx < len(weekly_tasks):
                task = weekly_tasks[task_idx]
                
                end_time = current_time + datetime.timedelta(hours=task["duration"])
                
                daily_schedule[date_str].append({
                    "subject": task["subject"],
                    "topic": task["topic"],
                    "start_time": current_time.strftime("%H:%M"),
                    "end_time": end_time.strftime("%H:%M"),
                    "duration": task["duration"]
                })
                
                # Add break
                current_time = end_time + datetime.timedelta(minutes=15)
                task_idx += 1
                sessions_today += 1
                
        current_date += datetime.timedelta(days=7)
        
    return daily_schedule

def generate_weekly_plan(courses_data: Dict[str, Any], exam_dates: Dict[str, str], user_preferences: Dict[str, Any], start_date_str: str) -> Dict[str, Any]:
    """
    Generates a comprehensive weekly plan.
    """
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    available_hours = 4 # Default
    
    # 1. Calculate Hours
    course_schedule = calculate_study_hours(courses_data, exam_dates, available_hours)
    
    # 2. Optimize Slots
    daily_slots = optimize_time_slots(course_schedule, user_preferences, start_date)
    
    # 3. Add Revision and Mock Tests
    for course, date_str in exam_dates.items():
        exam_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Mock Test (1 day before)
        mock_date = exam_date - datetime.timedelta(days=1)
        mock_date_str = mock_date.isoformat()
        if mock_date_str not in daily_slots:
            daily_slots[mock_date_str] = []
        daily_slots[mock_date_str].append({
            "subject": course,
            "topic": "FULL MOCK TEST",
            "start_time": "09:00",
            "end_time": "12:00",
            "duration": 3.0
        })
        
        # Revision (2 days before)
        rev_date = exam_date - datetime.timedelta(days=2)
        rev_date_str = rev_date.isoformat()
        if rev_date_str not in daily_slots:
            daily_slots[rev_date_str] = []
        daily_slots[rev_date_str].append({
            "subject": course,
            "topic": "FINAL REVISION",
            "start_time": "09:00",
            "end_time": "12:00",
            "duration": 3.0
        })
        
    return {
        "course_analysis": course_schedule,
        "daily_schedule": daily_slots
    }
