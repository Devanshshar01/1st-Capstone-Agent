import logging
from typing import Dict, Any
from tools.scheduler_tools import calculate_study_hours, optimize_time_slots, generate_weekly_plan
from tools.memory_tools import save_user_profile

logger = logging.getLogger(__name__)

class SchedulerAgent:
    """
    Agent responsible for creating optimized study plans.
    Role: Schedule Creation Specialist
    """
    def __init__(self):
        logger.info("Scheduler Agent initialized.")

    def create_schedule(self, user_id: str, courses: Dict[str, Any], preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a study schedule based on courses and user preferences.
        """
        logger.info(f"Creating schedule for user {user_id}")
        
        # Extract exam dates
        exam_dates = {}
        for name, data in courses.items():
            if "exam_date" in data:
                exam_dates[name] = data["exam_date"]
        
        start_date = "2025-11-21" # Fixed start date
        
        try:
            plan = generate_weekly_plan(courses, exam_dates, preferences, start_date)
            
            # Save profile with new schedule (mock update)
            profile_data = {
                "courses": courses,
                "preferences": preferences,
                "current_schedule": plan
            }
            save_user_profile(user_id, profile_data)
            
            return {"status": "success", "schedule": plan}
        except Exception as e:
            logger.error(f"Error creating schedule: {e}")
            return {"status": "error", "message": str(e)}
