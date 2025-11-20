import logging
from typing import Dict, Any
from tools.progress_tools import track_session_completion, calculate_progress_metrics, identify_weak_areas, generate_progress_report

logger = logging.getLogger(__name__)

class ProgressAgent:
    """
    Agent responsible for tracking progress and providing insights.
    Tone: Encouraging and analytical.
    """
    def __init__(self):
        logger.info("Progress Agent initialized.")

    def log_progress(self, user_id: str, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Logs a completed session.
        """
        return track_session_completion(user_id, session_data, {"percentage": 100})

    def get_report(self, user_id: str) -> str:
        """
        Generates a text-based progress report.
        """
        return generate_progress_report(user_id)
    
    def get_insights(self, user_id: str) -> Dict[str, Any]:
        """
        Analyzes performance to find weak areas.
        """
        weak_areas = identify_weak_areas(user_id)
        metrics = calculate_progress_metrics(user_id)
        return {
            "weak_areas": weak_areas,
            "metrics": metrics,
            "message": f"You're making good progress! Focus on {weak_areas[0]} next." if weak_areas else "Great job across the board!"
        }
