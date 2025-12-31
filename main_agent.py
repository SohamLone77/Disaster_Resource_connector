from agents.planner import Planner
from agents.worker import Worker
from agents.evaluator import Evaluator
from core.context_engineering import ContextEngine
from core.observability import Observability
from core.a2a_protocol import Message, A2AProtocol
from memory.session_memory import SessionMemory
import logging
import time

class MainAgent:
    def __init__(self):
        self.planner = Planner()
        self.workers = {
            "shelter": Worker("shelter"),
            "food": Worker("food"), 
            "medical": Worker("medical"),
            "government": Worker("government")
        }
        self.evaluator = Evaluator()
        self.context_engine = ContextEngine()
        self.session_memory = SessionMemory()
        self.observability = Observability()
        self.a2a_protocol = A2AProtocol()
        
        self.setup_message_handlers()
    
    def setup_message_handlers(self):
        self.a2a_protocol.register_handler("planner", self.handle_planner_message)
        self.a2a_protocol.register_handler("worker", self.handle_worker_message)
        self.a2a_protocol.register_handler("evaluator", self.handle_evaluator_message)
    
    def handle_message(self, user_input: str, user_lat: float = None, user_lon: float = None) -> dict:
        start_time = time.time()
        
        session_id = self.session_memory.create_session(user_input)
        self.observability.log_agent_activity("main_agent", "process_start", session_id, {"user_input": user_input})
        
        # Pass user coordinates to the planner
        plan = self.planner.create_plan(user_input, session_id, user_lat, user_lon)
        
        worker_results = []
        all_map_resources = []
        
        for resource_type in plan.get("resource_types", []):
            if resource_type in self.workers:
                worker = self.workers[resource_type]
                result = worker.execute_task(plan)
                worker_results.append(result)
                
                # Collect resources for map display
                for item in result.get("results", []):
                    if item.get("lat") and item.get("lon"):
                        all_map_resources.append({
                            "type": resource_type,
                            "name": item.get("name", "Unknown"),
                            "address": item.get("address", ""),
                            "lat": item.get("lat"),
                            "lon": item.get("lon"),
                            "details": item.get("details", "")
                        })
        
        final_result = self.evaluator.evaluate_results(worker_results, plan)
        final_result["map_resources"] = all_map_resources
        
        end_time = time.time()
        self.observability.log_performance_metrics("handle_message", start_time, end_time, True)
        self.observability.log_agent_activity("main_agent", "process_complete", session_id, {
            "resource_count": final_result.get("resource_count", 0),
            "confidence": final_result.get("evaluation_confidence", 0)
        })
        
        return final_result
    
    def handle_planner_message(self, message: Message) -> dict:
        return {"status": "planner_message_processed"}
    
    def handle_worker_message(self, message: Message) -> dict:
        return {"status": "worker_message_processed"}
    
    def handle_evaluator_message(self, message: Message) -> dict:
        return {"status": "evaluator_message_processed"}

def run_agent(user_input: str):
    agent = MainAgent()
    result = agent.handle_message(user_input)
    return result["final_response"]

def run_agent_with_location(user_input: str, latitude: float = None, longitude: float = None):
    """Run agent with user's location for map display."""
    agent = MainAgent()
    result = agent.handle_message(user_input, latitude, longitude)
    return result["final_response"], result.get("map_resources", [])
