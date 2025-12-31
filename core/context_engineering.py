from memory.session_memory import SessionMemory
import re
from datetime import datetime

class ContextEngine:
    def __init__(self):
        self.session_memory = SessionMemory()
        # Common location keywords to extract
        self.location_keywords = [
            "downtown", "northside", "eastside", "westside", "central",
            "north", "south", "east", "west", "near", "close to",
            "in", "at", "around", "by the"
        ]
        self.area_mapping = {
            "north": "northside", "south": "downtown", 
            "east": "eastside", "west": "westside",
            "downtown": "downtown", "central": "central",
            "city": "central", "suburb": "northside"
        }
    
    def analyze_context(self, user_input: str, session_id: str, user_lat: float = None, user_lon: float = None) -> dict:
        session = self.session_memory.get_session(session_id)
        if not session:
            session_id = self.session_memory.create_session(user_input)
            session = self.session_memory.get_session(session_id)
        
        # Extract location from user input
        extracted_location = self._extract_location(user_input)
        urgency = self._detect_urgency(user_input)
        disaster_type = self._infer_disaster_type(user_input)
        
        context = {
            "session_id": session_id,
            "timestamp": session["created_at"],
            "location": {
                "area": extracted_location.get("area", "central"),
                "extracted_location": extracted_location.get("raw", ""),
                "coordinates": {"lat": user_lat, "lon": user_lon} if user_lat and user_lon else None,
                "user_lat": user_lat,
                "user_lon": user_lon,
                "needs_pets": self._check_pet_needs(user_input),
                "urgency": urgency
            },
            "urgency": urgency,
            "disaster_type": disaster_type,
            "user_needs": self._extract_needs(user_input),
            "current_time": datetime.now().strftime("%I:%M %p"),
            "user_input": user_input
        }
        
        # Update session with extracted context
        self.session_memory.update_session(session_id, {
            "location": context["location"],
            "disaster_type": disaster_type,
            "urgency": urgency
        })
        
        return context
    
    def _extract_location(self, user_input: str) -> dict:
        """Extract location information from user input"""
        input_lower = user_input.lower()
        extracted = {"area": "central", "raw": ""}
        
        # Check for direct area mentions
        for area_key, area_value in self.area_mapping.items():
            if area_key in input_lower:
                extracted["area"] = area_value
                extracted["raw"] = area_key
                break
        
        # Try to extract location phrases
        location_patterns = [
            r'(?:in|at|near|around|by)\s+(?:the\s+)?([a-zA-Z\s]+?)(?:\s+area|\s+neighborhood|\s+district|,|\.|$)',
            r'(?:located|location|from)\s+(?:in\s+)?([a-zA-Z\s]+?)(?:,|\.|$)',
            r'([a-zA-Z]+side)\b'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, input_lower)
            if match:
                location_text = match.group(1).strip()
                if len(location_text) > 2 and location_text not in ['the', 'a', 'an', 'my']:
                    extracted["raw"] = location_text
                    # Map to known areas
                    for area_key, area_value in self.area_mapping.items():
                        if area_key in location_text:
                            extracted["area"] = area_value
                            break
        
        return extracted
    
    def _check_pet_needs(self, user_input: str) -> bool:
        """Check if user mentions pets"""
        pet_keywords = ['pet', 'dog', 'cat', 'animal', 'pets']
        return any(word in user_input.lower() for word in pet_keywords)
    
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
