"""
Data storage module for persistent data:
- Missing persons registry
- Volunteer registration
- Resource requests
- SOS alerts
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import hashlib

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

MISSING_PERSONS_FILE = os.path.join(DATA_DIR, "missing_persons.json")
VOLUNTEERS_FILE = os.path.join(DATA_DIR, "volunteers.json")
RESOURCE_REQUESTS_FILE = os.path.join(DATA_DIR, "resource_requests.json")
SOS_ALERTS_FILE = os.path.join(DATA_DIR, "sos_alerts.json")
SAFE_REPORTS_FILE = os.path.join(DATA_DIR, "safe_reports.json")

def _load_json(filepath: str) -> list:
    try:
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return []

def _save_json(filepath: str, data: list):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ==================== MISSING PERSONS ====================
def report_missing_person(name: str, age: int, gender: str, description: str, 
                          last_seen_location: str, last_seen_time: str,
                          contact_name: str, contact_phone: str,
                          photo_url: str = "", lat: float = None, lon: float = None) -> dict:
    """Report a missing person."""
    persons = _load_json(MISSING_PERSONS_FILE)
    person_id = hashlib.md5(f"{name}{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper()
    
    new_person = {
        "id": person_id,
        "name": name,
        "age": age,
        "gender": gender,
        "description": description,
        "last_seen_location": last_seen_location,
        "last_seen_time": last_seen_time,
        "contact_name": contact_name,
        "contact_phone": contact_phone,
        "photo_url": photo_url,
        "lat": lat,
        "lon": lon,
        "status": "missing",
        "reported_at": datetime.now().isoformat(),
        "found_at": None
    }
    persons.append(new_person)
    _save_json(MISSING_PERSONS_FILE, persons)
    return new_person

def search_missing_persons(query: str = "", status: str = "missing") -> List[dict]:
    """Search missing persons by name or description."""
    persons = _load_json(MISSING_PERSONS_FILE)
    results = []
    query = query.lower()
    for p in persons:
        if status and p.get("status") != status:
            continue
        if not query or query in p.get("name", "").lower() or query in p.get("description", "").lower() or query in p.get("last_seen_location", "").lower():
            results.append(p)
    return sorted(results, key=lambda x: x.get("reported_at", ""), reverse=True)

def mark_person_found(person_id: str, found_location: str = "") -> bool:
    """Mark a missing person as found."""
    persons = _load_json(MISSING_PERSONS_FILE)
    for p in persons:
        if p.get("id") == person_id:
            p["status"] = "found"
            p["found_at"] = datetime.now().isoformat()
            p["found_location"] = found_location
            _save_json(MISSING_PERSONS_FILE, persons)
            return True
    return False

def get_missing_stats() -> dict:
    """Get statistics on missing persons."""
    persons = _load_json(MISSING_PERSONS_FILE)
    missing = len([p for p in persons if p.get("status") == "missing"])
    found = len([p for p in persons if p.get("status") == "found"])
    return {"total": len(persons), "missing": missing, "found": found}

# ==================== VOLUNTEERS ====================
def register_volunteer(name: str, phone: str, email: str, skills: List[str],
                       available_areas: str, availability: str,
                       has_vehicle: bool = False, lat: float = None, lon: float = None) -> dict:
    """Register a new volunteer."""
    volunteers = _load_json(VOLUNTEERS_FILE)
    vol_id = hashlib.md5(f"{phone}{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper()
    
    new_volunteer = {
        "id": vol_id,
        "name": name,
        "phone": phone,
        "email": email,
        "skills": skills,
        "available_areas": available_areas,
        "availability": availability,
        "has_vehicle": has_vehicle,
        "lat": lat,
        "lon": lon,
        "status": "active",
        "registered_at": datetime.now().isoformat(),
        "tasks_completed": 0
    }
    volunteers.append(new_volunteer)
    _save_json(VOLUNTEERS_FILE, volunteers)
    return new_volunteer

def search_volunteers(skill: str = "", area: str = "") -> List[dict]:
    """Search volunteers by skill or area."""
    volunteers = _load_json(VOLUNTEERS_FILE)
    results = []
    for v in volunteers:
        if v.get("status") != "active":
            continue
        skill_match = not skill or skill.lower() in [s.lower() for s in v.get("skills", [])]
        area_match = not area or area.lower() in v.get("available_areas", "").lower()
        if skill_match and area_match:
            results.append(v)
    return results

def get_volunteer_stats() -> dict:
    """Get volunteer statistics."""
    volunteers = _load_json(VOLUNTEERS_FILE)
    active = len([v for v in volunteers if v.get("status") == "active"])
    with_vehicle = len([v for v in volunteers if v.get("has_vehicle")])
    return {"total": len(volunteers), "active": active, "with_vehicle": with_vehicle}

# ==================== RESOURCE REQUESTS ====================
def create_resource_request(requester_name: str, phone: str, resource_type: str,
                            description: str, urgency: str, quantity: int = 1,
                            location: str = "", lat: float = None, lon: float = None) -> dict:
    """Create a new resource request."""
    requests = _load_json(RESOURCE_REQUESTS_FILE)
    req_id = hashlib.md5(f"{phone}{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper()
    
    new_request = {
        "id": req_id,
        "requester_name": requester_name,
        "phone": phone,
        "resource_type": resource_type,
        "description": description,
        "urgency": urgency,
        "quantity": quantity,
        "location": location,
        "lat": lat,
        "lon": lon,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "fulfilled_at": None,
        "fulfilled_by": None
    }
    requests.append(new_request)
    _save_json(RESOURCE_REQUESTS_FILE, requests)
    return new_request

def get_resource_requests(status: str = "", resource_type: str = "") -> List[dict]:
    """Get resource requests with optional filters."""
    requests = _load_json(RESOURCE_REQUESTS_FILE)
    results = []
    for r in requests:
        if status and r.get("status") != status:
            continue
        if resource_type and r.get("resource_type") != resource_type:
            continue
        results.append(r)
    return sorted(results, key=lambda x: (x.get("urgency") == "critical", x.get("created_at")), reverse=True)

def fulfill_resource_request(request_id: str, fulfilled_by: str) -> bool:
    """Mark a resource request as fulfilled."""
    requests = _load_json(RESOURCE_REQUESTS_FILE)
    for r in requests:
        if r.get("id") == request_id:
            r["status"] = "fulfilled"
            r["fulfilled_at"] = datetime.now().isoformat()
            r["fulfilled_by"] = fulfilled_by
            _save_json(RESOURCE_REQUESTS_FILE, requests)
            return True
    return False

def get_request_stats() -> dict:
    """Get resource request statistics."""
    requests = _load_json(RESOURCE_REQUESTS_FILE)
    pending = len([r for r in requests if r.get("status") == "pending"])
    fulfilled = len([r for r in requests if r.get("status") == "fulfilled"])
    critical = len([r for r in requests if r.get("urgency") == "critical" and r.get("status") == "pending"])
    return {"total": len(requests), "pending": pending, "fulfilled": fulfilled, "critical": critical}

# ==================== SOS ALERTS ====================
def create_sos_alert(name: str, phone: str, emergency_type: str, message: str,
                     lat: float, lon: float) -> dict:
    """Create an SOS emergency alert."""
    alerts = _load_json(SOS_ALERTS_FILE)
    alert_id = hashlib.md5(f"{phone}{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper()
    
    new_alert = {
        "id": alert_id,
        "name": name,
        "phone": phone,
        "emergency_type": emergency_type,
        "message": message,
        "lat": lat,
        "lon": lon,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "resolved_at": None
    }
    alerts.append(new_alert)
    _save_json(SOS_ALERTS_FILE, alerts)
    return new_alert

def get_active_sos_alerts() -> List[dict]:
    """Get all active SOS alerts."""
    alerts = _load_json(SOS_ALERTS_FILE)
    return [a for a in alerts if a.get("status") == "active"]

def resolve_sos_alert(alert_id: str) -> bool:
    """Mark an SOS alert as resolved."""
    alerts = _load_json(SOS_ALERTS_FILE)
    for a in alerts:
        if a.get("id") == alert_id:
            a["status"] = "resolved"
            a["resolved_at"] = datetime.now().isoformat()
            _save_json(SOS_ALERTS_FILE, alerts)
            return True
    return False

# ==================== SAFE REPORTS ("I'M SAFE") ====================
def report_safe(name: str, phone: str, location: str, message: str = "",
                lat: float = None, lon: float = None) -> dict:
    """Report that someone is safe."""
    reports = _load_json(SAFE_REPORTS_FILE)
    
    new_report = {
        "name": name,
        "phone": phone,
        "location": location,
        "message": message,
        "lat": lat,
        "lon": lon,
        "reported_at": datetime.now().isoformat()
    }
    reports.append(new_report)
    _save_json(SAFE_REPORTS_FILE, reports)
    return new_report

def search_safe_reports(name: str = "", phone: str = "") -> List[dict]:
    """Search safe reports by name or phone."""
    reports = _load_json(SAFE_REPORTS_FILE)
    results = []
    for r in reports:
        if name and name.lower() not in r.get("name", "").lower():
            continue
        if phone and phone not in r.get("phone", ""):
            continue
        results.append(r)
    return sorted(results, key=lambda x: x.get("reported_at", ""), reverse=True)

# ==================== DONATIONS ====================
DONATIONS_FILE = os.path.join(DATA_DIR, "donations.json")

def register_donation(donor_name: str, phone: str, donation_type: str,
                      items: str, quantity: str, pickup_location: str,
                      lat: float = None, lon: float = None) -> dict:
    """Register a donation offer."""
    donations = _load_json(DONATIONS_FILE)
    don_id = hashlib.md5(f"{phone}{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper()
    
    new_donation = {
        "id": don_id,
        "donor_name": donor_name,
        "phone": phone,
        "donation_type": donation_type,
        "items": items,
        "quantity": quantity,
        "pickup_location": pickup_location,
        "lat": lat,
        "lon": lon,
        "status": "available",
        "created_at": datetime.now().isoformat()
    }
    donations.append(new_donation)
    _save_json(DONATIONS_FILE, donations)
    return new_donation

def get_available_donations(donation_type: str = "") -> List[dict]:
    """Get available donations."""
    donations = _load_json(DONATIONS_FILE)
    results = [d for d in donations if d.get("status") == "available"]
    if donation_type:
        results = [d for d in results if d.get("donation_type") == donation_type]
    return results
