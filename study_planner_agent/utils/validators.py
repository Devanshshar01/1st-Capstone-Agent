import datetime
from typing import Any, Dict, List, Optional

def validate_date_format(date_str: str) -> bool:
    """Validates if a string is in YYYY-MM-DD format."""
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_future_date(date_str: str) -> bool:
    """Validates if a date is in the future."""
    if not validate_date_format(date_str):
        return False
    
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    return date_obj >= datetime.date.today()

def validate_course_data(course_data: Dict[str, Any]) -> bool:
    """Validates the structure of course data."""
    required_keys = ["topics", "difficulty"]
    for key in required_keys:
        if key not in course_data:
            return False
            
    if not isinstance(course_data["topics"], list) or not course_data["topics"]:
        return False
        
    if course_data["difficulty"] not in ["high", "medium", "low"]:
        return False
        
    return True
