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
        # Add urgency to location context for filtering
        location['urgency'] = plan.get('priority', 'medium')
        
        # Check if user mentioned pets in their input
        user_input = plan.get('user_input', '').lower()
        location['needs_pets'] = any(word in user_input for word in ['pet', 'dog', 'cat', 'animal'])
        
        return {
            "resource_type": "shelter",
            "results": self.tools.find_nearby_shelters(location),
            "confidence": 0.85,
            "timestamp": plan.get('timestamp')
        }
    
    def _find_food_distribution(self, plan: dict) -> dict:
        location = plan.get('location_constraints', {})
        location['urgency'] = plan.get('priority', 'medium')
        
        return {
            "resource_type": "food",
            "results": self.tools.find_food_distribution_points(location),
            "confidence": 0.80,
            "timestamp": plan.get('timestamp')
        }
    
    def _find_medical_aid(self, plan: dict) -> dict:
        location = plan.get('location_constraints', {})
        location['urgency'] = plan.get('priority', 'medium')
        
        return {
            "resource_type": "medical",
            "results": self.tools.find_medical_aid_stations(location),
            "confidence": 0.90,
            "timestamp": plan.get('timestamp')
        }
    
    def _find_government_aid(self, plan: dict) -> dict:
        # Extract disaster type from context if available
        user_input = plan.get('user_input', '').lower()
        disaster_type = 'general'
        
        disaster_keywords = {
            "hurricane": ["hurricane", "storm", "flood"],
            "earthquake": ["earthquake", "tremor"],
            "wildfire": ["fire", "wildfire"],
            "tornado": ["tornado", "twister"]
        }
        
        for dtype, keywords in disaster_keywords.items():
            if any(kw in user_input for kw in keywords):
                disaster_type = dtype
                break
        
        return {
            "resource_type": "government",
            "results": self.tools.get_disaster_aid_instructions(disaster_type),
            "confidence": 0.95,
            "timestamp": plan.get('timestamp')
        }
