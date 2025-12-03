from dataclasses import dataclass
from typing import Dict, Any, Optional
import uuid
import time

@dataclass
class Message:
    message_id: str
    session_id: str
    from_agent: str
    to_agent: str
    message_type: str
    payload: Dict[str, Any]
    timestamp: float
    priority: str = "medium"
    
    def __post_init__(self):
        if not self.message_id:
            self.message_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = time.time()

class A2AProtocol:
    def __init__(self):
        self.message_queue = []
        self.handlers = {}
    
    def send_message(self, message: Message):
        self.message_queue.append(message)
        self.message_queue.sort(key=lambda x: (x.priority != "high", x.timestamp))
    
    def receive_message(self, agent_name: str) -> Optional[Message]:
        for i, message in enumerate(self.message_queue):
            if message.to_agent == agent_name:
                return self.message_queue.pop(i)
        return None
    
    def register_handler(self, agent_name: str, handler_function):
        self.handlers[agent_name] = handler_function
    
    def process_messages(self):
        processed_messages = []
        for message in self.message_queue[:]:
            if message.to_agent in self.handlers:
                handler = self.handlers[message.to_agent]
                try:
                    result = handler(message)
                    processed_messages.append(message.message_id)
                except Exception as e:
                    print(f"Error processing message {message.message_id}: {e}")
        
        self.message_queue = [msg for msg in self.message_queue if msg.message_id not in processed_messages]
