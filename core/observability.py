import logging
import time
from datetime import datetime
import os

class Observability:
    def __init__(self):
        self.setup_logging()
        
    def setup_logging(self):
        handlers = [logging.StreamHandler()]
        
        # Only add file handler if we have write permissions (not on Hugging Face)
        try:
            if os.access('.', os.W_OK):
                handlers.append(logging.FileHandler('agent_system.log'))
        except:
            pass
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=handlers
        )
    
    def log_agent_activity(self, agent_name: str, action: str, session_id: str, details: dict = None):
        logger = logging.getLogger(agent_name)
        log_data = {
            "agent": agent_name,
            "action": action,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        logger.info(f"Agent Activity: {log_data}")
    
    def log_performance_metrics(self, operation: str, start_time: float, end_time: float, success: bool = True):
        duration = end_time - start_time
        logger = logging.getLogger("performance")
        logger.info(f"Performance - Operation: {operation}, Duration: {duration:.2f}s, Success: {success}")
