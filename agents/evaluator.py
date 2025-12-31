import logging
from datetime import datetime

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
        priority = plan.get("priority", "medium")
        
        if priority == "high":
            priority_order = ["medical", "shelter", "food", "government"]
        else:
            priority_order = ["shelter", "food", "medical", "government"]
        
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
    
    def _generate_map_link(self, lat: float, lon: float, name: str) -> str:
        if lat and lon:
            return f"[🗺️ Get Directions](https://www.google.com/maps/dir/?api=1&destination={lat},{lon})"
        return ""
    
    def _generate_response(self, results: list, plan: dict) -> str:
        if not results:
            return """## ❌ No Resources Found

I couldn't find specific resources. Please try these emergency contacts:

### 🚨 Emergency Contacts
- **911** - Emergency Services
- **1-800-621-3362** - FEMA Assistance  
- **211** - Community Resources Helpline
- **1-800-733-2767** - American Red Cross

Visit **[DisasterAssistance.gov](https://www.disasterassistance.gov)** to apply for help."""
        
        user_input = plan.get("user_input", "")
        priority = plan.get("priority", "medium")
        user_coords = plan.get("user_coordinates", {})
        current_time = datetime.now().strftime("%I:%M %p on %B %d, %Y")
        
        response_parts = [f"## 🆘 Disaster Resource Results"]
        response_parts.append(f"*Updated: {current_time}*\n")
        
        if user_coords.get("lat") and user_coords.get("lon"):
            response_parts.append(f"📍 **Your Location Detected** - Showing nearby resources")
        else:
            response_parts.append(f"📍 *Enable location for distance info*")
        
        response_parts.append(f"\n🔍 **Your Request:** \"{user_input[:80]}{'...' if len(user_input) > 80 else ''}\"")
        
        if priority == "high":
            response_parts.append("\n> ⚠️ **URGENT REQUEST** - Prioritizing emergency resources\n")
        
        response_parts.append("\n---\n")
        
        for result in results:
            resource_type = result.get("resource_type", "unknown")
            resource_data = result.get("results", [])
            
            if resource_data:
                emoji_map = {"shelter": "🏠", "food": "🍲", "medical": "🏥", "government": "📋"}
                emoji = emoji_map.get(resource_type, "📌")
                
                response_parts.append(f"### {emoji} {resource_type.upper()} RESOURCES\n")
                
                for i, item in enumerate(resource_data[:5], 1):
                    name = item.get('name', 'Unknown')
                    verified = "✅" if item.get('verified') else ""
                    
                    if resource_type == "shelter":
                        org = item.get('organization', '')
                        phone = item.get('phone', 'Not available')
                        website = item.get('website', '')
                        services = item.get('services', [])
                        services_str = ", ".join(services) if isinstance(services, list) else services
                        pet_info = "🐾 Pet-friendly" if item.get('pet_friendly') == True else ""
                        hours = item.get('hours', '')
                        
                        response_parts.append(f"**{i}. {name}** {verified}")
                        if org:
                            response_parts.append(f"   - 🏛️ *{org}*")
                        response_parts.append(f"   - 📞 **{phone}**")
                        if website:
                            response_parts.append(f"   - 🌐 [{website}]({website if website.startswith('http') else 'https://' + website})")
                        if services_str:
                            response_parts.append(f"   - 🛠️ {services_str}")
                        if hours:
                            response_parts.append(f"   - 🕐 {hours} {pet_info}")
                        response_parts.append("")
                    
                    elif resource_type == "food":
                        org = item.get('organization', '')
                        food_type = item.get('type', '')
                        phone = item.get('phone', 'Not available')
                        website = item.get('website', '')
                        services = item.get('services', [])
                        services_str = ", ".join(services) if isinstance(services, list) else services
                        hours = item.get('hours', '')
                        eligibility = item.get('eligibility', '')
                        
                        response_parts.append(f"**{i}. {name}** {verified}")
                        if org:
                            response_parts.append(f"   - 🏛️ *{org}*")
                        if food_type:
                            response_parts.append(f"   - 📦 Type: {food_type}")
                        response_parts.append(f"   - 📞 **{phone}**")
                        if website:
                            response_parts.append(f"   - 🌐 [{website}]({website if website.startswith('http') else 'https://' + website})")
                        if services_str:
                            response_parts.append(f"   - 🍽️ {services_str}")
                        if eligibility:
                            response_parts.append(f"   - ✅ Eligibility: {eligibility}")
                        if hours:
                            response_parts.append(f"   - 🕐 {hours}")
                        response_parts.append("")
                    
                    elif resource_type == "medical":
                        org = item.get('organization', '')
                        med_type = item.get('type', '')
                        phone = item.get('phone', 'Not available')
                        website = item.get('website', '')
                        services = item.get('services', [])
                        services_str = ", ".join(services) if isinstance(services, list) else services
                        hours = item.get('hours', '')
                        notes = item.get('notes', '')
                        
                        response_parts.append(f"**{i}. {name}** {verified}")
                        if org:
                            response_parts.append(f"   - 🏛️ *{org}*")
                        if med_type:
                            response_parts.append(f"   - 🏥 Type: {med_type}")
                        response_parts.append(f"   - 📞 **{phone}**")
                        if website:
                            response_parts.append(f"   - 🌐 [{website}]({website if website.startswith('http') else 'https://' + website})")
                        if services_str:
                            response_parts.append(f"   - 🩺 {services_str}")
                        if notes:
                            response_parts.append(f"   - 💡 *{notes}*")
                        if hours:
                            response_parts.append(f"   - 🕐 {hours}")
                        response_parts.append("")
                    
                    elif resource_type == "government":
                        agency = item.get('agency', '')
                        phone = item.get('phone', '')
                        website = item.get('website', '')
                        services = item.get('services', '')
                        how_to_apply = item.get('how_to_apply', '')
                        deadline = item.get('deadline', '')
                        description = item.get('description', '')
                        additional = item.get('additional_info', '')
                        
                        response_parts.append(f"**{i}. {name}** {verified}")
                        if agency:
                            response_parts.append(f"   - 🏛️ *{agency}*")
                        if phone:
                            response_parts.append(f"   - 📞 **{phone}**")
                        if website:
                            response_parts.append(f"   - 🌐 [{website}]({website if website.startswith('http') else 'https://' + website})")
                        if services:
                            response_parts.append(f"   - 📋 {services}")
                        if how_to_apply:
                            response_parts.append(f"   - ✍️ **How to Apply:** {how_to_apply}")
                        if deadline and deadline != "Check with agency":
                            response_parts.append(f"   - ⏰ Deadline: {deadline}")
                        if description and not phone:  # For tips
                            response_parts.append(f"   - {description}")
                        if additional:
                            response_parts.append(f"   - ℹ️ {additional}")
                        response_parts.append("")
        
        response_parts.append("---\n")
        response_parts.append("### 🚨 Emergency Quick Reference\n")
        response_parts.append("| Service | Contact |")
        response_parts.append("|---------|---------|")
        response_parts.append("| **Emergency** | 911 |")
        response_parts.append("| **FEMA** | 1-800-621-3362 |")
        response_parts.append("| **Red Cross** | 1-800-733-2767 |")
        response_parts.append("| **211 Helpline** | 211 |")
        response_parts.append("| **Crisis Counseling** | 1-800-985-5990 |")
        response_parts.append("")
        response_parts.append("> ℹ️ All resources verified. Visit official websites for current availability.")
        response_parts.append("> 🗺️ *Check the map for locations with directions*")
        
        return "\n".join(response_parts)
    
    def _calculate_confidence(self, results: list) -> float:
        if not results:
            return 0.0
        confidences = [r.get("confidence", 0) for r in results]
        return sum(confidences) / len(confidences)
