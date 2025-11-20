import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OrchestratorAgent:
    """
    Main coordinator agent that routes user requests to appropriate sub-agents.
    """
    def __init__(self):
        self.agents = {}
        logger.info("Orchestrator Agent initialized.")

    def register_agent(self, name: str, agent: Any):
        """Registers a sub-agent with the orchestrator."""
        self.agents[name] = agent
        logger.info(f"Registered agent: {name}")

    def process_request(self, user_input: str, user_id: str) -> str:
        """
        Analyzes user input and delegates to the appropriate agent.
        """
        logger.info(f"Processing request for user {user_id}: {user_input}")
        
        # Simple routing logic for demo purposes
        # In a real app, this would use Gemini to classify intent
        
        if "progress" in user_input.lower():
            if "progress" in self.agents:
                return self.agents["progress"].get_report(user_id)
        
        if "motivate" in user_input.lower():
            if "reminder" in self.agents:
                self.agents["reminder"].motivate(user_id)
                return "Motivation sent!"
                
        return "I'm listening. You can ask for 'progress' or 'motivate me', or use the /schedule command to create a plan."
