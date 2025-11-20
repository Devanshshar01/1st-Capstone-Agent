import logging
import os
import sys
from config import LOG_LEVEL

def setup_logger(name="study_planner"):
    """Configures and returns a logger instance."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(LOG_LEVEL)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console Handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File Handler (optional, could add later)
        
    return logger
