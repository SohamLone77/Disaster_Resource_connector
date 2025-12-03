class ResourceTools:
    def __init__(self):
        self.shelter_data = [
            {"name": "Central High School Shelter", "description": "Emergency shelter with capacity for 200 people", "location": "downtown"},
            {"name": "Community Center", "description": "Shelter with basic amenities and food", "location": "northside"},
            {"name": "Red Cross Shelter", "description": "Medical staff available, pet-friendly", "location": "eastside"}
        ]
        
        self.food_data = [
            {"name": "Food Distribution Center", "description": "Daily meals and water distribution", "location": "central"},
            {"name": "Mobile Kitchen Unit", "description": "Hot meals available 24/7", "location": "downtown"},
            {"name": "Community Church", "description": "Food pantry and bottled water", "location": "westside"}
        ]
        
        self.medical_data = [
            {"name": "Field Hospital", "description": "Emergency medical care and supplies", "location": "central"},
            {"name": "Mobile Medical Unit", "description": "Basic first aid and medication", "location": "downtown"},
            {"name": "Urgent Care Center", "description": "Extended hours for emergency cases", "location": "northside"}
        ]
        
        self.government_data = [
            {"name": "FEMA Assistance", "description": "Apply online at disasterassistance.gov or call 1-800-621-FEMA"},
            {"name": "Disaster Relief", "description": "Emergency funding and support programs available"},
            {"name": "Emergency Housing", "description": "Temporary housing assistance programs"}
        ]
    
    def find_nearby_shelters(self, location: dict) -> list:
        return self.shelter_data
    
    def find_food_distribution_points(self, location: dict) -> list:
        return self.food_data
    
    def find_medical_aid_stations(self, location: dict) -> list:
        return self.medical_data
    
    def get_disaster_aid_instructions(self, agency: str = "FEMA") -> list:
        return self.government_data
