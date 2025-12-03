from memory.session_memory import SessionMemory
import re

class ContextEngine:
    def __init__(self):
        self.session_memory = SessionMemory()
    
    def analyze_context(self, user_input: str, session_id: str) -> dict:
        session = self.session_memory.get_session(session_id)
        if not session:
            session_id = self.session_memory.create_session(user_input)
            session = self.session_memory.get_session(session_id)
        
        context = {
            "session_id": session_id,
            "timestamp": session["created_at"],
            "location": session.get("location", {}),
            "urgency": self._detect_urgency(user_input),
            "disaster_type": self._infer_disaster_type(user_input),
            "user_needs": self._extract_needs(user_input)
        }
        
        return context
    
    def _detect_urgency(self, user_input: str) -> str:
        urgent_patterns = [r'emergency', r'urgent', r'right now', r'immediately', r'critical']
        for pattern in urgent_patterns:
            if re.search(pattern, user_input.lower()):
                return "high"
        return "medium"
    
    def _infer_disaster_type(self, user_input: str) -> str:
        disaster_keywords = {
            "hurricane": ["hurricane", "storm", "flood"],
            "earthquake": ["earthquake", "tremor", "shake"],
            "wildfire": ["fire", "wildfire", "smoke"],
            "tornado": ["tornado", "twister"]
        }
        
        input_lower = user_input.lower()
        for disaster_type, keywords in disaster_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                return disaster_type
        return "general"
    
    def _extract_needs(self, user_input: str) -> list:
        needs = []
        need_patterns = {
            "shelter": ["shelter", "place to stay", "housing", "home"],
            "food": ["food", "hungry", "eat", "water", "thirsty"],
            "medical": ["medical", "doctor", "hospital", "medicine", "hurt", "injured"],
            "assistance": ["help", "aid", "assistance", "fema", "government"]
        }
        
        input_lower = user_input.lower()
        for need_type, patterns in need_patterns.items():
            if any(pattern in input_lower for pattern in patterns):
                needs.append(need_type)
                
        return needs if needs else ["shelter", "food", "medical"]
