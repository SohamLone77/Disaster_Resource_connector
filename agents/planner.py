from core.context_engineering import ContextEngine
import logging
import time

class Planner:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.context_engine = ContextEngine()
        
    def create_plan(self, user_input: str, session_id: str, user_lat: float = None, user_lon: float = None) -> dict:
        self.logger.info(f"Planner creating plan for session {session_id}")
        
        context = self.context_engine.analyze_context(user_input, session_id, user_lat, user_lon)
        
        plan = {
            "session_id": session_id,
            "user_input": user_input,
            "resource_types": self._identify_resource_types(user_input),
            "priority": self._determine_priority(user_input),
            "location_constraints": context.get("location", {}),
            "user_coordinates": {"lat": user_lat, "lon": user_lon},
            "timestamp": context.get("timestamp")
        }
        
        self.logger.info(f"Plan created: {plan}")
        return plan
    
    def _identify_resource_types(self, user_input: str) -> list:
        input_lower = user_input.lower()
        resource_types = []
        
        if any(word in input_lower for word in ['shelter', 'place to stay', 'housing']):
            resource_types.append("shelter")
        if any(word in input_lower for word in ['food', 'water', 'hungry', 'thirsty']):
            resource_types.append("food")
        if any(word in input_lower for word in ['medical', 'doctor', 'hospital', 'medicine']):
            resource_types.append("medical")
        if any(word in input_lower for word in ['fema', 'aid', 'assistance', 'government']):
            resource_types.append("government")
            
        return resource_types if resource_types else ["shelter", "food", "medical", "government"]
    
    def _determine_priority(self, user_input: str) -> str:
        urgent_keywords = ['emergency', 'urgent', 'immediately', 'now', 'critical']
        if any(word in user_input.lower() for word in urgent_keywords):
            return "high"
        return "medium"
