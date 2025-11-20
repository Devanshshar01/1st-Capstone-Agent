import sys
import os
import argparse
import platform
import logging
import time
import json
from colorama import init, Fore, Style
import google.generativeai as genai

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.orchestrator import OrchestratorAgent
from agents.scheduler_agent import SchedulerAgent
from agents.reschedule_agent import RescheduleAgent
from agents.progress_agent import ProgressAgent
from agents.reminder_agent import ReminderAgent
from agents.context_agent import ContextAgent
from utils.logger import setup_logger
from config import GOOGLE_API_KEY, DATA_DIR

# Initialize colorama
init(autoreset=True)

# Setup logger
logger = setup_logger()

ASCII_ART = f"""
{Fore.CYAN}
   _____ _           _       {Fore.MAGENTA}_____  _                             
  {Fore.CYAN}/ ____| |         | |     {Fore.MAGENTA}|  __ \| |                            
 {Fore.CYAN}| (___ | |_ _   __| |_   _ {Fore.MAGENTA}| |__) | | __ _ _ __  _ __   ___ _ __ 
  {Fore.CYAN}\___ \| __| | | |/ _` | | | |{Fore.MAGENTA}  ___/| |/ _` | '_ \| '_ \ / _ \ '__|
  {Fore.CYAN}____) | |_| |_| | (_| | |_| |{Fore.MAGENTA} |    | | (_| | | | | | | |  __/ |   
 {Fore.CYAN}|_____/ \__|\__,_|\__,_|\__, |{Fore.MAGENTA}_|    |_|\__,_|_| |_|_| |_|\___|_|   
                         {Fore.CYAN} __/ |                                      
                        {Fore.CYAN}|___/                                       
{Style.RESET_ALL}
"""

def check_system_requirements() -> bool:
    """Performs startup checks for the application."""
    print(f"{Fore.BLUE}Performing system checks...{Style.RESET_ALL}")
    
    # 1. Check Python Version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 10):
        logger.critical(f"Python 3.10+ is required. Found: {platform.python_version()}")
        return False
    logger.info(f"Python version check passed: {platform.python_version()}")

    # 2. Check API Key
    if not GOOGLE_API_KEY:
        logger.critical("GOOGLE_API_KEY not found in environment variables.")
        return False
    
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        logger.info("Google API Key configured.")
    except Exception as e:
        logger.critical(f"Failed to configure Google API: {e}")
        return False

    # 3. Check Data Directories
    if not os.path.exists(DATA_DIR):
        try:
            os.makedirs(DATA_DIR)
            logger.info(f"Created data directory: {DATA_DIR}")
        except OSError as e:
            logger.critical(f"Failed to create data directory: {e}")
            return False

    print(f"{Fore.GREEN}System checks passed!{Style.RESET_ALL}")
    return True

def initialize_agents() -> OrchestratorAgent:
    """Initializes and registers all agents."""
    print(f"{Fore.BLUE}Initializing agents...{Style.RESET_ALL}")
    
    orchestrator = OrchestratorAgent()
    
    agents = {
        "scheduler": SchedulerAgent(),
        "rescheduler": RescheduleAgent(),
        "progress": ProgressAgent(),
        "reminder": ReminderAgent(),
        "context": ContextAgent(data_dir=DATA_DIR)
    }
    
    for name, agent in agents.items():
        orchestrator.register_agent(name, agent)
        
    logger.info("All agents initialized and registered.")
    return orchestrator

def collect_schedule_input():
    """Interactive wizard to collect schedule data."""
    print(f"\n{Fore.YELLOW}=== Schedule Creation Wizard ==={Style.RESET_ALL}")
    
    courses = {}
    while True:
        name = input(f"\n{Fore.CYAN}Enter Course Name (or 'done' to finish): {Style.RESET_ALL}").strip()
        if name.lower() == 'done':
            if not courses:
                print("Please add at least one course.")
                continue
            break
            
        topics_str = input(f"Enter topics for {name} (comma separated): ").strip()
        topics = [t.strip() for t in topics_str.split(",") if t.strip()]
        
        difficulty = input(f"Difficulty (High/Medium/Low): ").strip().lower()
        if difficulty not in ['high', 'medium', 'low']:
            difficulty = 'medium'
            
        exam_date = input(f"Exam Date (YYYY-MM-DD): ").strip()
        
        courses[name] = {
            "topics": topics,
            "difficulty": difficulty,
            "exam_date": exam_date
        }
        
    print(f"\n{Fore.CYAN}Preferences:{Style.RESET_ALL}")
    daily_hours = input("Max daily study hours (default 5): ").strip()
    daily_hours = int(daily_hours) if daily_hours.isdigit() else 5
    
    peak_pref = input("Peak hours (Morning/Afternoon/Evening): ").strip().lower()
    
    return courses, {"daily_max_hours": daily_hours, "peak_hours": peak_pref}

def run_cli(orchestrator: OrchestratorAgent):
    """Runs the Command Line Interface."""
    print(ASCII_ART)
    print(f"{Fore.GREEN}Welcome to your Personal Study Planner AI Agent!{Style.RESET_ALL}")
    print(f"Type {Fore.YELLOW}/help{Style.RESET_ALL} for available commands.")
    
    user_id = "student_01"
    
    while True:
        try:
            user_input = input(f"\n{Fore.CYAN}You:{Style.RESET_ALL} ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['/quit', '/exit', 'exit', 'quit']:
                print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                break
                
            if user_input.lower() == '/help':
                print(f"\n{Fore.YELLOW}Available Commands:{Style.RESET_ALL}")
                print("  /help      - Show this help message")
                print("  /schedule  - Create a new study plan")
                print("  /progress  - Show progress report")
                print("  /quit      - Exit the application")
                continue
            
            if user_input.lower() == '/schedule':
                courses, prefs = collect_schedule_input()
                print(f"\n{Fore.BLUE}Generating schedule...{Style.RESET_ALL}")
                result = orchestrator.agents['scheduler'].create_schedule(user_id, courses, prefs)
                
                if result['status'] == 'success':
                    print(f"{Fore.GREEN}Schedule created successfully!{Style.RESET_ALL}")
                    # print(json.dumps(result['schedule']['daily_schedule'], indent=2)) # Too verbose
                    print(f"Plan covers {len(result['schedule']['daily_schedule'])} days.")
                    print("Check 'data/users/student_01.json' for full details.")
                else:
                    print(f"{Fore.RED}Error: {result['message']}{Style.RESET_ALL}")
                continue

            # Process request via orchestrator
            response = orchestrator.process_request(user_input, user_id)
            print(f"{Fore.MAGENTA}Agent:{Style.RESET_ALL} {response}")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
            break
        except Exception as e:
            logger.error(f"Runtime error: {e}")
            print(f"{Fore.RED}An error occurred. Please try again.{Style.RESET_ALL}")

def run_web():
    """Placeholder for Web UI."""
    print(f"{Fore.BLUE}Starting Web UI...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}NOTE: To use the ADK Web UI, please run the specific ADK command.{Style.RESET_ALL}")
    print("For this demo, we are simulating a web server startup.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping Web UI...")

def main():
    parser = argparse.ArgumentParser(description="Personal Study Planner AI Agent")
    parser.add_argument('--mode', choices=['cli', 'web'], default='cli', help='Run mode: cli or web')
    parser.add_argument('--demo', action='store_true', help='Run in demo mode with pre-seeded data')
    
    args = parser.parse_args()
    
    if not check_system_requirements():
        sys.exit(1)
        
    orchestrator = initialize_agents()
    
    if args.demo:
        print(f"{Fore.YELLOW}Running in DEMO mode...{Style.RESET_ALL}")
        from data.demo_data import DEMO_USER_PROFILE
        print("Loading demo profile...")
        orchestrator.agents['scheduler'].create_schedule("demo_user", DEMO_USER_PROFILE["courses"], DEMO_USER_PROFILE["preferences"])
        print(f"{Fore.GREEN}Demo schedule created!{Style.RESET_ALL}")
        
    if args.mode == 'cli':
        run_cli(orchestrator)
    elif args.mode == 'web':
        run_web()

if __name__ == "__main__":
    main()
