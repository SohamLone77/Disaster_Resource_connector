import logging

class Evaluator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def evaluate_results(self, worker_results: list, plan: dict) -> dict:
        self.logger.info("Evaluator processing worker results")
        
        prioritized_results = self._prioritize_resources(worker_results, plan)
        validated_results = self._validate_consistency(prioritized_results)
        final_response = self._generate_response(validated_results, plan)
        
        return {
            "session_id": plan.get("session_id"),
            "final_response": final_response,
            "resource_count": len(validated_results),
            "evaluation_confidence": self._calculate_confidence(validated_results)
        }
    
    def _prioritize_resources(self, results: list, plan: dict) -> list:
        priority_order = ["shelter", "medical", "food", "government"]
        prioritized = []
        
        for resource_type in priority_order:
            for result in results:
                if result.get("resource_type") == resource_type:
                    prioritized.append(result)
                    
        return prioritized
    
    def _validate_consistency(self, results: list) -> list:
        validated = []
        for result in results:
            if result.get("confidence", 0) > 0.5:
                validated.append(result)
        return validated
    
    def _generate_response(self, results: list, plan: dict) -> str:
        if not results:
            return "I'm sorry, but I couldn't find any available resources in your area. Please try emergency services or check official government channels."
        
        response_parts = ["Here are the available resources I found:"]
        
        for result in results:
            resource_type = result.get("resource_type", "unknown")
            resource_data = result.get("results", [])
            
            if resource_data:
                response_parts.append(f"\n{resource_type.title()} Resources:")
                for item in resource_data[:3]:
                    response_parts.append(f"• {item.get('name', 'Unknown')}: {item.get('description', 'No description')}")
        
        response_parts.append("\nPlease verify this information with official sources as conditions may change rapidly.")
        
        return "\n".join(response_parts)
    
    def _calculate_confidence(self, results: list) -> float:
        if not results:
            return 0.0
        confidences = [r.get("confidence", 0) for r in results]
        return sum(confidences) / len(confidences)
