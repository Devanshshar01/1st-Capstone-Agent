from typing import List, Dict, Any

def calculate_completion_rate(completed_sessions: int, total_sessions: int) -> float:
    """
    Calculates the percentage of completed study sessions.
    """
    if total_sessions == 0:
        return 0.0
    return (completed_sessions / total_sessions) * 100

def identify_weak_areas(performance_data: List[Dict[str, Any]]) -> List[str]:
    """
    Identifies subjects or topics where the user is struggling.
    """
    weak_areas = []
    for entry in performance_data:
        if entry.get('score', 100) < 70:
            weak_areas.append(entry.get('subject', 'Unknown'))
    return weak_areas
