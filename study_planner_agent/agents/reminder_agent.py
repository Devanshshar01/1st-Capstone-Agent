import logging
from typing import Dict, Any
from tools.notification_tools import schedule_reminder, send_notification, get_upcoming_reminders, generate_motivational_message

logger = logging.getLogger(__name__)

class ReminderAgent:
    """
    Agent responsible for sending notifications and motivation.
    """
    def __init__(self):
        logger.info("Reminder Agent initialized.")

    def send_alert(self, user_id: str, message: str, title: str = "Alert"):
        """
        Sends an immediate alert.
        """
        send_notification(user_id, {"title": title, "message": message})

    def check_reminders(self, user_id: str):
        """
        Checks and displays upcoming reminders.
        """
        reminders = get_upcoming_reminders(user_id)
        for rem in reminders:
            self.send_alert(user_id, rem["message"], rem["title"])
            
    def motivate(self, user_id: str):
        """
        Sends a motivational message.
        """
        msg = generate_motivational_message({})
        self.send_alert(user_id, msg, "Motivation")
