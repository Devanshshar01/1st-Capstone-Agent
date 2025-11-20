import datetime
from typing import Dict, Any

def schedule_notification(user_id: str, message: str, time: datetime.datetime) -> bool:
    """
    Schedules a notification for a specific time.
    """
    print(f"Scheduled notification for {user_id} at {time}: {message}")
    return True

def send_instant_notification(user_id: str, message: str) -> bool:
    """
    Sends an immediate notification.
    """
    print(f"Sent notification to {user_id}: {message}")
    return True
