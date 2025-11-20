import json
import os

def create_demo_data(data_dir: str = "./data"):
    """
    Creates demo data for users and schedules.
    """
    users_dir = os.path.join(data_dir, "users")
    os.makedirs(users_dir, exist_ok=True)
    
    demo_user = {
        "id": "student_01",
        "name": "Alex",
        "preferences": {
            "study_hours_per_day": 4,
            "preferred_times": ["morning", "evening"]
        },
        "courses": [
            {"name": "CS101", "difficulty": 2, "credits": 3},
            {"name": "MATH202", "difficulty": 3, "credits": 4}
        ]
    }
    
    with open(os.path.join(users_dir, "student_01.json"), 'w') as f:
        json.dump(demo_user, f, indent=4)
        
    print("Demo data created.")

if __name__ == "__main__":
    create_demo_data()
