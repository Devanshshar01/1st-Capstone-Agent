import logging
from typing import List

logger = logging.getLogger(__name__)

class ReminderAgent:
    """
    Agent sends notifications and motivational messages.
    """
    def __init__(self):
        logger.info("Reminder Agent initialized.")

    def send_reminder(self, user_id: str, message: str):
        """
        Sends a reminder to the user.
        """
        logger.info(f"Sending reminder to {user_id}: {message}")
        # TODO: Implement notification delivery (e.g., print to console for CLI)
        print(f"NOTIFICATION: {message}")

    def get_pending_reminders(self, user_id: str) -> List[str]:
        """
        Retrieves pending reminders.
        """
        return []
