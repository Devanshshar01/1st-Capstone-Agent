import datetime
import math
from typing import List, Dict, Any, Optional
from config import DIFFICULTY_MULTIPLIERS, SESSION_DEFAULTS, PEAK_HOURS_MAP

def calculate_study_hours(courses_data: Dict[str, Any], exam_dates: Dict[str, str], available_hours_per_day: int) -> Dict[str, Any]:
    """
    Calculates optimal study time distribution based on syllabus and exam schedule.
    
    Algorithm:
    1. Calculate days until exam from current date (2025-11-21).
    2. Calculate total hours needed: (num_topics * 4 hours) * difficulty_multiplier.
    3. Distribute hours across weeks, reserving 2 days for revision.
    """
    schedule_data = {}
    # Fixed start date as per requirements
    current_date = datetime.date(2025, 11, 21)
    
    for course_name, data in courses_data.items():
        exam_date_str = exam_dates.get(course_name)
        if not exam_date_str:
            continue
            
        exam_date = datetime.datetime.strptime(exam_date_str, "%Y-%m-%d").date()
        days_until_exam = (exam_date - current_date).days
        
        if days_until_exam <= 0:
            continue
            
        # Reserve 2 days for revision
        study_days = max(1, days_until_exam - 2)
        
        # Calculate base hours needed
        # Base: number of topics * 4 hours
        num_topics = len(data.get("topics", []))
        base_hours = num_topics * 4
        
        difficulty = data.get("difficulty", "medium").lower()
        multiplier = DIFFICULTY_MULTIPLIERS.get(difficulty, 1.0)
        
        total_hours_needed = base_hours * multiplier
        
        # Adjust for progress (if any)
        progress = data.get("current_progress", 0.0)
        total_hours_needed *= (1.0 - progress)
        
        # Calculate weekly distribution
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
            "exam_date": exam_date_str,
            "study_days": study_days
        }
        
    return schedule_data

def optimize_time_slots(course_schedule: Dict[str, Any], user_preferences: Dict[str, Any], start_date_str: str = "2025-11-21") -> Dict[str, List[Dict[str, Any]]]:
    """
    Generates specific time slots for study sessions.
    
    Algorithm:
    1. Convert weekly hours to daily sessions.
    2. Assign specific time slots (08:00, 10:00, 14:00, 17:00).
    3. Balance subjects across days.
    4. Include 15-minute breaks.
    """
    daily_schedule = {}
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    current_date = start_date
    
    preferred_days = user_preferences.get("preferred_days", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    session_duration = user_preferences.get("session_duration", 2)
    daily_max_hours = user_preferences.get("daily_max_hours", 5)
    
    # Define standard slots based on peak preference "morning" (6-12)
    # Slots: 08:00, 10:00, 14:00, 17:00
    standard_slots = [
        datetime.time(8, 0),
        datetime.time(10, 15), # 2h + 15m break
        datetime.time(14, 0),
        datetime.time(17, 0)
    ]
    
    # Plan for 6 weeks (until Jan 2)
    for week_num in range(6):
        # Gather weekly tasks
        weekly_tasks = []
        for course, data in course_schedule.items():
            hours_list = data.get("hours_per_week", [])
            if week_num < len(hours_list):
                hours = hours_list[week_num]
                num_sessions = math.ceil(hours / session_duration)
                topics = list(data.get("topics_distribution", {}).keys())
                
                for i in range(num_sessions):
                    topic = topics[i % len(topics)] if topics else "General Study"
                    weekly_tasks.append({
                        "subject": course,
                        "topic": topic,
                        "duration": session_duration
                    })
        
        # Sort tasks to balance subjects (simple shuffle or round robin)
        # Here we just interleave them if possible
        
        # Distribute across preferred days
        days_in_week = []
        for i in range(7):
            day_date = current_date + datetime.timedelta(days=i)
            if day_date.strftime("%A") in preferred_days:
                days_in_week.append(day_date)
        
        task_idx = 0
        for day_date in days_in_week:
            date_str = day_date.isoformat()
            if date_str not in daily_schedule:
                daily_schedule[date_str] = []
            
            hours_today = 0
            slot_idx = 0
            
            # Avoid same subject twice in a row logic could go here
            last_subject = None
            
            while hours_today < daily_max_hours and task_idx < len(weekly_tasks) and slot_idx < len(standard_slots):
                task = weekly_tasks[task_idx]
                
                # Simple check to avoid same subject consecutive (if possible)
                if task["subject"] == last_subject and task_idx + 1 < len(weekly_tasks):
                    # Swap with next
                    weekly_tasks[task_idx], weekly_tasks[task_idx+1] = weekly_tasks[task_idx+1], weekly_tasks[task_idx]
                    task = weekly_tasks[task_idx]
                
                start_time = datetime.datetime.combine(day_date, standard_slots[slot_idx])
                end_time = start_time + datetime.timedelta(hours=task["duration"])
                
                daily_schedule[date_str].append({
                    "subject": task["subject"],
                    "topic": task["topic"],
                    "start_time": start_time.strftime("%H:%M"),
                    "end_time": end_time.strftime("%H:%M"),
                    "duration": task["duration"]
                })
                
                hours_today += task["duration"]
                last_subject = task["subject"]
                task_idx += 1
                slot_idx += 1
                
        current_date += datetime.timedelta(days=7)
        
    return daily_schedule

def generate_weekly_plan(courses_data: Dict[str, Any], exam_dates: Dict[str, str], user_preferences: Dict[str, Any], start_date_str: str = "2025-11-21") -> Dict[str, Any]:
    """
    Generates a comprehensive weekly plan including revision and mock tests.
    """
    available_hours = user_preferences.get("daily_max_hours", 5)
    
    # 1. Calculate Hours
    course_schedule = calculate_study_hours(courses_data, exam_dates, available_hours)
    
    # 2. Optimize Slots
    daily_slots = optimize_time_slots(course_schedule, user_preferences, start_date_str)
    
    # 3. Add Revision (2 days before) and Mock Tests (1 day before)
    for course, date_str in exam_dates.items():
        exam_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Mock Test (1 day before)
        mock_date = exam_date - datetime.timedelta(days=1)
        mock_date_str = mock_date.isoformat()
        
        # Clear existing slots for mock test day to prioritize it
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
        
        # Clear existing slots for revision day
        daily_slots[rev_date_str] = []
        
        daily_slots[rev_date_str].append({
            "subject": course,
            "topic": "FINAL REVISION",
            "start_time": "09:00",
            "end_time": "12:00",
            "duration": 3.0
        })
        
    # 4. Add Weekly Progress Checkpoint (Sunday 18:00)
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    current = start_date
    end_date = datetime.date(2026, 1, 2)
    
    while current <= end_date:
        if current.strftime("%A") == "Sunday":
            d_str = current.isoformat()
            if d_str not in daily_slots:
                daily_slots[d_str] = []
            daily_slots[d_str].append({
                "subject": "General",
                "topic": "Weekly Progress Checkpoint",
                "start_time": "18:00",
                "end_time": "18:30",
                "duration": 0.5
            })
        current += datetime.timedelta(days=1)

    return {
        "course_analysis": course_schedule,
        "daily_schedule": daily_slots,
        "statistics": {
            "total_courses": len(courses_data),
            "start_date": start_date_str,
            "end_date": "2026-01-02"
        }
    }
