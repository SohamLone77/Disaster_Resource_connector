from tools.tools import ResourceTools
import logging

class Worker:
    def __init__(self, worker_type: str):
        self.worker_type = worker_type
        self.logger = logging.getLogger(__name__)
        self.tools = ResourceTools()
        
    def execute_task(self, plan: dict) -> dict:
        self.logger.info(f"{self.worker_type} worker executing task")
        
        if self.worker_type == "shelter":
            return self._find_shelters(plan)
        elif self.worker_type == "food":
            return self._find_food_distribution(plan)
        elif self.worker_type == "medical":
            return self._find_medical_aid(plan)
        elif self.worker_type == "government":
            return self._find_government_aid(plan)
        else:
            return {"error": f"Unknown worker type: {self.worker_type}"}
    
    def _find_shelters(self, plan: dict) -> dict:
        location = plan.get('location_constraints', {})
        return {
            "resource_type": "shelter",
            "results": self.tools.find_nearby_shelters(location),
            "confidence": 0.85,
            "timestamp": plan.get('timestamp')
        }
    
    def _find_food_distribution(self, plan: dict) -> dict:
        location = plan.get('location_constraints', {})
        return {
            "resource_type": "food",
            "results": self.tools.find_food_distribution_points(location),
            "confidence": 0.80,
            "timestamp": plan.get('timestamp')
        }
    
    def _find_medical_aid(self, plan: dict) -> dict:
        location = plan.get('location_constraints', {})
        return {
            "resource_type": "medical",
            "results": self.tools.find_medical_aid_stations(location),
            "confidence": 0.90,
            "timestamp": plan.get('timestamp')
        }
    
    def _find_government_aid(self, plan: dict) -> dict:
        return {
            "resource_type": "government",
            "results": self.tools.get_disaster_aid_instructions(),
            "confidence": 0.95,
            "timestamp": plan.get('timestamp')
        }
