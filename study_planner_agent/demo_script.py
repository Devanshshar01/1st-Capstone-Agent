import time
import sys
import os
from colorama import init, Fore, Style

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import initialize_agents
from data.demo_data import DEMO_USER_PROFILE

init(autoreset=True)

def print_agent(agent_name, message):
    print(f"\n{Fore.MAGENTA}{agent_name}:{Style.RESET_ALL} {message}")
    time.sleep(1.5)

def print_user(message):
    print(f"\n{Fore.CYAN}User:{Style.RESET_ALL} {message}")
    time.sleep(1)

def run_demo():
    print(f"{Fore.YELLOW}=== STARTING DEMO SCENARIO ==={Style.RESET_ALL}")
    time.sleep(1)
    
    orchestrator = initialize_agents()
    user_id = "demo_user"
    
    # Act 1: Onboarding & Schedule Creation
    print(f"\n{Fore.GREEN}--- ACT 1: Schedule Creation ---{Style.RESET_ALL}")
    print_user("I need a study plan for my BCA exams starting Dec 22nd.")
    print_agent("Orchestrator", "I can help with that. Let's create a schedule based on your subjects.")
    
    print(f"\n{Fore.BLUE}[System] Loading demo profile...{Style.RESET_ALL}")
    result = orchestrator.agents['scheduler'].create_schedule(user_id, DEMO_USER_PROFILE["courses"], DEMO_USER_PROFILE["preferences"])
    
    if result['status'] == 'success':
        print_agent("Scheduler", "I've generated a plan for you. Here's a summary:")
        schedule = result['schedule']['daily_schedule']
        print(f"Total Study Days: {len(schedule)}")
        print("First week preview:")
        count = 0
        for date, sessions in schedule.items():
            if count >= 3: break
            print(f"  {date}:")
            for s in sessions:
                print(f"    - {s['start_time']} to {s['end_time']}: {s['subject']} ({s['topic']})")
            count += 1
            
    # Act 2: Progress Tracking
    print(f"\n{Fore.GREEN}--- ACT 2: Progress Update ---{Style.RESET_ALL}")
    print_user("How am I doing so far?")
    report = orchestrator.agents['progress'].get_report(user_id)
    print_agent("Progress", f"Here is your current status:\n{report}")
    
    # Act 3: Missed Session
    print(f"\n{Fore.GREEN}--- ACT 3: Handling Missed Sessions ---{Style.RESET_ALL}")
    print_user("I missed my Discrete Math session yesterday.")
    missed = [{"subject": "Discrete Mathematics", "topic": "Logic", "date": "2025-11-22"}]
    response = orchestrator.agents['rescheduler'].handle_missed_session(user_id, missed)
    print_agent("Rescheduler", response['message'])
    print(f"Proposed Alternative: {response['proposed_alternatives'][0]['suggested_slot']['date']} at {response['proposed_alternatives'][0]['suggested_slot']['start_time']}")
    
    # Act 4: Motivation
    print(f"\n{Fore.GREEN}--- ACT 4: Motivation ---{Style.RESET_ALL}")
    print_user("I'm feeling overwhelmed.")
    orchestrator.agents['reminder'].motivate(user_id)
    
    print(f"\n{Fore.YELLOW}=== DEMO COMPLETED ==={Style.RESET_ALL}")

if __name__ == "__main__":
    run_demo()
