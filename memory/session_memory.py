import uuid
import time
from datetime import datetime

class SessionMemory:
    def __init__(self):
        self.sessions = {}
        self.cache = {}
        
    def create_session(self, user_input: str) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "session_id": session_id,
            "created_at": datetime.now(),
            "user_input": user_input,
            "location": self._extract_location(user_input),
            "interactions": [],
            "last_accessed": time.time()
        }
        return session_id
    
    def get_session(self, session_id: str) -> dict:
        session = self.sessions.get(session_id)
        if session:
            session["last_accessed"] = time.time()
        return session
    
    def update_session(self, session_id: str, updates: dict):
        if session_id in self.sessions:
            self.sessions[session_id].update(updates)
            self.sessions[session_id]["last_accessed"] = time.time()
    
    def cache_resource_data(self, key: str, data: list, ttl: int = 3600):
        self.cache[key] = {
            "data": data,
            "timestamp": time.time(),
            "ttl": ttl
        }
    
    def get_cached_data(self, key: str) -> list:
        cached = self.cache.get(key)
        if cached and (time.time() - cached["timestamp"]) < cached["ttl"]:
            return cached["data"]
        return None
    
    def _extract_location(self, user_input: str) -> dict:
        location_keywords = ["downtown", "northside", "eastside", "westside", "central"]
        for location in location_keywords:
            if location in user_input.lower():
                return {"area": location, "coordinates": None}
        return {"area": "central", "coordinates": None}
