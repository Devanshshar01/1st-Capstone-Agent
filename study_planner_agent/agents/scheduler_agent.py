import logging
import datetime
from typing import Dict, Any, List
from tools.scheduler_tools import generate_weekly_plan

logger = logging.getLogger(__name__)

class SchedulerAgent:
    """
    Agent responsible for creating optimized study plans.
    """
    def __init__(self):
        logger.info("Scheduler Agent initialized.")

    def create_schedule(self, user_id: str, courses: Dict[str, Any], preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a study schedule based on courses and user preferences.
        """
        logger.info(f"Creating schedule for user {user_id}")
        
        # Extract necessary data from input
        # Assuming 'courses' input matches the detailed format or we adapt it
        # For this demo, we'll assume the input is already structured or we mock the missing parts
        
        # Mock exam dates if not present (in a real app, this would come from user input)
        exam_dates = {name: "2025-12-20" for name in courses.keys()} 
        
        start_date = datetime.date.today().isoformat()
        
        try:
            plan = generate_weekly_plan(courses, exam_dates, preferences, start_date)
            return {"status": "success", "schedule": plan}
        except Exception as e:
            logger.error(f"Error creating schedule: {e}")
            return {"status": "error", "message": str(e)}
