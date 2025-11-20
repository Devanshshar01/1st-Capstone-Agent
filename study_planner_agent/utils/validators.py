from typing import Dict, Any, List

def validate_user_profile(profile: Dict[str, Any]) -> bool:
    """
    Validates the structure of a user profile.
    """
    required_keys = ["id", "name", "preferences", "courses"]
    return all(key in profile for key in required_keys)

def validate_course(course: Dict[str, Any]) -> bool:
    """
    Validates a course object.
    """
    required_keys = ["name", "difficulty", "credits"]
    return all(key in course for key in required_keys)
