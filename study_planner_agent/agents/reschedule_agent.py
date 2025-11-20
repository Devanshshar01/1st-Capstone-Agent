import logging
from typing import Dict, Any, List
from tools.reschedule_tools import detect_conflicts, find_alternative_slots, rebalance_schedule
from tools.memory_tools import load_user_profile

logger = logging.getLogger(__name__)

class RescheduleAgent:
    """
    Agent responsible for handling missed sessions and urgent changes.
    Tone: Empathetic and supportive.
    """
    def __init__(self):
        logger.info("Reschedule Agent initialized.")

    def handle_missed_session(self, user_id: str, missed_sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes missed sessions and proposes a new schedule.
        """
        logger.info(f"Handling missed sessions for user {user_id}")
        
        profile = load_user_profile(user_id)
        current_schedule = profile.get("current_schedule", {}).get("daily_schedule", {})
        
        # 1. Detect Conflicts
        conflicts = detect_conflicts(current_schedule, missed_sessions, None)
        
        # 2. Find Alternatives
        alternatives = find_alternative_slots(current_schedule, missed_sessions, {})
        
        # 3. Rebalance (Mock logic)
        # In a real scenario, we'd ask the user to confirm alternatives first
        
        return {
            "status": "success",
            "conflicts": conflicts,
            "proposed_alternatives": alternatives,
            "message": "I understand things come up. Here are some options to get back on track."
        }
