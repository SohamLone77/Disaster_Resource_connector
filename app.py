import gradio as gr
from main_agent import run_agent_with_location
from tools.tools import ResourceTools
import data_store
import logging
import folium
from folium.plugins import MarkerCluster
from datetime import datetime

logging.basicConfig(level=logging.INFO)
tools = ResourceTools()

# Multi-language support
LANGUAGES = {
    "en": {
        "title": "🆘 Disaster Resource Connector",
        "emergency": "Emergency", "shelter": "Shelter", "food": "Food", "medical": "Medical",
        "find_resources": "Find Resources", "your_location": "Your Location",
        "detect_location": "📍 Detect My Location", "describe_situation": "Describe your situation",
        "quick_actions": "Quick Actions", "weather": "Weather", "blood_bank": "Blood Banks",
        "missing_persons": "Missing Persons", "volunteer": "Volunteer", "donate": "Donate",
        "preparedness": "Preparedness", "sos": "🆘 SOS", "im_safe": "✅ I'm Safe"
    },
    "hi": {
        "title": "🆘 आपदा संसाधन कनेक्टर",
        "emergency": "आपातकाल", "shelter": "आश्रय", "food": "भोजन", "medical": "चिकित्सा",
        "find_resources": "संसाधन खोजें", "your_location": "आपका स्थान",
        "detect_location": "📍 मेरा स्थान पता करें", "describe_situation": "अपनी स्थिति बताएं",
        "quick_actions": "त्वरित कार्रवाई", "weather": "मौसम", "blood_bank": "ब्लड बैंक",
        "missing_persons": "लापता व्यक्ति", "volunteer": "स्वयंसेवक", "donate": "दान करें",
        "preparedness": "तैयारी", "sos": "🆘 एसओएस", "im_safe": "✅ मैं सुरक्षित हूं"
    },
    "mr": {
        "title": "🆘 आपत्ती संसाधन कनेक्टर",
        "emergency": "आणीबाणी", "shelter": "निवारा", "food": "अन्न", "medical": "वैद्यकीय",
        "find_resources": "संसाधने शोधा", "your_location": "तुमचे स्थान",
        "detect_location": "📍 माझे स्थान शोधा", "describe_situation": "तुमची परिस्थिती सांगा",
        "quick_actions": "जलद कृती", "weather": "हवामान", "blood_bank": "रक्तपेढी",
        "missing_persons": "बेपत्ता व्यक्ती", "volunteer": "स्वयंसेवक", "donate": "दान करा",
        "preparedness": "तयारी", "sos": "🆘 एसओएस", "im_safe": "✅ मी सुरक्षित आहे"
    },
    "ta": {
        "title": "🆘 பேரிடர் வள இணைப்பான்",
        "emergency": "அவசரம்", "shelter": "தங்குமிடம்", "food": "உணவு", "medical": "மருத்துவம்",
        "find_resources": "வளங்களைக் கண்டறியவும்", "your_location": "உங்கள் இருப்பிடம்",
        "detect_location": "📍 என் இருப்பிடத்தைக் கண்டறியவும்", "describe_situation": "உங்கள் நிலையை விவரிக்கவும்",
        "quick_actions": "விரைவு செயல்கள்", "weather": "வானிலை", "blood_bank": "இரத்த வங்கி",
        "missing_persons": "காணாமல் போனவர்கள்", "volunteer": "தன்னார்வலர்", "donate": "நன்கொடை",
        "preparedness": "தயார்நிலை", "sos": "🆘 எஸ்ஓஎஸ்", "im_safe": "✅ நான் பாதுகாப்பாக இருக்கிறேன்"
    }
}

def get_text(key: str, lang: str = "en") -> str:
    return LANGUAGES.get(lang, LANGUAGES["en"]).get(key, key)

def create_map(user_lat, user_lon, resources=None, zoom=12):
    if not user_lat or not user_lon:
        user_lat, user_lon = 20.5937, 78.9629
        zoom = 5
    
    m = folium.Map(location=[user_lat, user_lon], zoom_start=zoom, tiles='OpenStreetMap')
    
    if zoom >= 10:
        folium.Marker([user_lat, user_lon], popup="📍 Your Location", tooltip="You are here",
                      icon=folium.Icon(color='red', icon='home', prefix='glyphicon')).add_to(m)
        folium.Circle([user_lat, user_lon], radius=3000, color='red', fill=True, fill_opacity=0.1).add_to(m)
    
    if resources:
        colors = {'shelter': 'blue', 'food': 'green', 'medical': 'purple', 'blood': 'darkred', 'hospital': 'purple'}
        icons = {'shelter': 'home', 'food': 'apple', 'medical': 'plus-sign', 'blood': 'tint', 'hospital': 'plus-sign'}
        cluster = MarkerCluster().add_to(m)
        
        for r in resources:
            if r.get("lat") and r.get("lon"):
                rtype = r.get("type", "shelter")
                popup = f"<b>{r.get('name', 'Unknown')}</b><br>{r.get('phone', '')}<br><a href='https://www.google.com/maps/dir/?api=1&destination={r['lat']},{r['lon']}' target='_blank'>🗺️ Directions</a>"
                folium.Marker([r["lat"], r["lon"]], popup=popup, tooltip=r.get("name", "Resource"),
                              icon=folium.Icon(color=colors.get(rtype, 'gray'), icon=icons.get(rtype, 'info-sign'), prefix='glyphicon')).add_to(cluster)
    
    legend = '''<div style="position:fixed;bottom:30px;left:30px;z-index:1000;background:white;padding:10px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.2);font-size:12px;"><b>🗺️ Legend</b><br>🔴 You<br>🔵 Shelter<br>🟢 Food<br>🟣 Medical<br>🔴 Blood Bank</div>'''
    m.get_root().html.add_child(folium.Element(legend))
    return m._repr_html_()

def process_request(message, lat, lon):
    try:
        if not message or not message.strip():
            return "⚠️ Please describe what you need", create_map(lat, lon)
        response, resources = run_agent_with_location(message, lat, lon)
        return response, create_map(lat, lon, resources)
    except Exception as e:
        return f"❌ Error: {str(e)}", create_map(lat, lon)

def get_weather_display(lat, lon):
    if not lat or not lon:
        return "📍 Please detect your location first"
    weather = tools.get_weather_alerts(lat, lon)
    current = weather.get("current", {})
    alerts = weather.get("alerts", [])
    forecast = weather.get("forecast", [])
    
    # Get recent verified disasters
    recent_disasters = tools.get_recent_disasters()
    active_alerts = [d for d in recent_disasters if "ACTIVE" in d.get("status", "") or "SEVERE" in d.get("status", "")]
    
    result = f"""## 🌤️ Current Weather (Live from Open-Meteo)
**Condition:** {current.get('condition', 'N/A')}
**Temperature:** {current.get('temp', 'N/A')}°C
**Humidity:** {current.get('humidity', 'N/A')}%
**Wind:** {current.get('wind', 'N/A')} km/h

"""
    if alerts:
        result += "## ⚠️ Weather Alerts\n"
        for a in alerts:
            result += f"**{a['level']}**: {a['message']}\n"
    
    # Add verified disaster alerts
    if active_alerts:
        result += "\n---\n## 🚨 ACTIVE DISASTER ALERTS (Verified - Dec 2025)\n"
        for d in active_alerts:
            result += f"""
### {d['status']} {d['event']}
- **Date:** {d['date']}
- **Affected Areas:** {', '.join(d.get('areas', []))}
- **Description:** {d.get('description', 'N/A')}
- **Source:** ✅ {d.get('source', 'Official')} ([View]({d.get('source_url', '#')}))
"""
            if d.get('actions'):
                result += "- **Actions:** " + " | ".join(d['actions']) + "\n"
    
    if forecast:
        result += "\n---\n## 📅 5-Day Forecast\n| Day | High | Low | Rain |\n|-----|------|-----|------|\n"
        for f in forecast:
            result += f"| {f['day']} | {f['high']}°C | {f['low']}°C | {f['rain']} |\n"
    
    result += "\n---\n### ✅ Data Sources\n- **Weather:** Open-Meteo API (Real-time)\n- **Disaster Alerts:** India Meteorological Department, ReliefWeb, NDRF\n- **Last Updated:** " + datetime.now().strftime("%d %b %Y %H:%M IST")
    
    return result

def get_blood_banks_display(lat, lon):
    if not lat or not lon:
        return "📍 Please detect your location first", create_map(lat, lon)
    banks = tools.find_blood_banks(lat, lon)
    result = "## 🩸 Blood Banks Near You\n\n"
    for i, b in enumerate(banks[:5], 1):
        result += f"""### {i}. {b['name']}
📞 **Phone:** {b.get('phone', 'N/A')}
🌐 **Website:** {b.get('website', 'N/A')}
📏 **Distance:** {b.get('distance', 'N/A')}

"""
    result += "\n### 🩸 Blood Donation Portals\n- **eRaktKosh:** https://eraktkosh.in/\n- **Indian Red Cross:** https://indianredcross.org/\n"
    for b in banks:
        b["type"] = "blood"
    return result, create_map(lat, lon, banks)

def get_preparedness_display(disaster_type):
    checklist = tools.get_preparedness_checklist(disaster_type)
    first_aid = tools.get_first_aid_guide()
    evac = tools.get_evacuation_info(None, None)
    
    result = f"## {checklist['title']}\n\n"
    for item in checklist['items']:
        result += f"- [ ] {item}\n"
    
    result += "\n---\n## 🩹 First Aid Quick Guide\n"
    for fa in first_aid:
        result += f"### {fa['title']}\n{fa['steps']}\n\n"
    
    result += "---\n## 🚨 Evacuation Tips\n"
    for tip in evac['tips']:
        result += f"- {tip}\n"
    
    result += "\n### Emergency Helplines\n"
    for name, number in evac['helplines'].items():
        result += f"- **{name}:** {number}\n"
    
    return result

def report_missing(name, age, gender, description, last_location, last_time, contact_name, contact_phone, lat, lon):
    if not name or not contact_phone:
        return "❌ Name and contact phone are required"
    person = data_store.report_missing_person(name, age, gender, description, last_location, last_time, contact_name, contact_phone, "", lat, lon)
    return f"""✅ **Missing Person Reported Successfully**

**Report ID:** {person['id']}
**Name:** {name}
**Status:** Missing

Please share this ID with authorities and search teams. Call **100** (Police) to file an official report.
"""

def search_missing(query):
    persons = data_store.search_missing_persons(query)
    if not persons:
        return "No missing persons found matching your search."
    result = f"## 🔍 Missing Persons ({len(persons)} found)\n\n"
    for p in persons:
        status_emoji = "🔴" if p['status'] == 'missing' else "🟢"
        result += f"""### {status_emoji} {p['name']} (ID: {p['id']})
- **Age:** {p['age']} | **Gender:** {p['gender']}
- **Last Seen:** {p['last_seen_location']} at {p['last_seen_time']}
- **Description:** {p['description']}
- **Contact:** {p['contact_name']} - {p['contact_phone']}

"""
    return result

def register_vol(name, phone, email, skills, areas, availability, has_vehicle, lat, lon):
    if not name or not phone:
        return "❌ Name and phone are required"
    skills_list = [s.strip() for s in skills.split(",") if s.strip()]
    vol = data_store.register_volunteer(name, phone, email, skills_list, areas, availability, has_vehicle, lat, lon)
    return f"""✅ **Volunteer Registered Successfully!**

**Volunteer ID:** {vol['id']}
**Name:** {name}
**Skills:** {', '.join(skills_list)}

Thank you for volunteering! You may be contacted during emergencies.
"""

def create_request(name, phone, resource_type, description, urgency, quantity, location, lat, lon):
    if not name or not phone:
        return "❌ Name and phone are required"
    req = data_store.create_resource_request(name, phone, resource_type, description, urgency, quantity, location, lat, lon)
    return f"""✅ **Resource Request Created**

**Request ID:** {req['id']}
**Type:** {resource_type}
**Urgency:** {urgency}
**Status:** Pending

Volunteers and relief workers will be notified.
"""

def view_requests():
    requests = data_store.get_resource_requests(status="pending")
    if not requests:
        return "No pending resource requests."
    result = "## 📋 Pending Resource Requests\n\n"
    for r in requests:
        urgency_emoji = "🔴" if r['urgency'] == 'critical' else "🟡" if r['urgency'] == 'high' else "🟢"
        result += f"""### {urgency_emoji} {r['resource_type'].upper()} - {r['description'][:50]}...
- **Requester:** {r['requester_name']} | **Phone:** {r['phone']}
- **Location:** {r['location']}
- **Quantity:** {r['quantity']} | **Request ID:** {r['id']}

"""
    return result

def send_sos(name, phone, emergency_type, message, lat, lon):
    if not lat or not lon:
        return "❌ Location required for SOS! Please detect your location first."
    alert = data_store.create_sos_alert(name, phone, emergency_type, message, lat, lon)
    return f"""# 🆘 SOS ALERT SENT!

**Alert ID:** {alert['id']}
**Location:** {lat:.6f}, {lon:.6f}
**Type:** {emergency_type}

## 📞 CALL EMERGENCY SERVICES NOW:
- **112** - Universal Emergency
- **100** - Police
- **102/108** - Ambulance
- **101** - Fire

Your location has been recorded. Share this with responders!

**Google Maps:** https://www.google.com/maps?q={lat},{lon}
"""

def report_safe_status(name, phone, location, message, lat, lon):
    report = data_store.report_safe(name, phone, location, message, lat, lon)
    return f"""# ✅ SAFETY STATUS REPORTED

**Name:** {name}
**Location:** {location}
**Time:** {report['reported_at']}

Your family and friends can now find you in the "Search Safe Reports" section.
"""

def search_safe(name, phone):
    reports = data_store.search_safe_reports(name, phone)
    if not reports:
        return "No safe reports found."
    result = "## ✅ Safe Reports Found\n\n"
    for r in reports:
        result += f"""### ✅ {r['name']}
- **Phone:** {r['phone']}
- **Location:** {r['location']}
- **Reported:** {r['reported_at']}
- **Message:** {r.get('message', 'N/A')}

"""
    return result

def register_donation(name, phone, donation_type, items, quantity, location, lat, lon):
    if not name or not phone:
        return "❌ Name and phone are required"
    donation = data_store.register_donation(name, phone, donation_type, items, quantity, location, lat, lon)
    return f"""✅ **Donation Registered!**

**Donation ID:** {donation['id']}
**Type:** {donation_type}
**Items:** {items}

Relief workers will contact you for pickup. Thank you for your generosity! 🙏
"""

def create_app():
    with gr.Blocks(title="🆘 Disaster Resource Connector") as app:
        # Header
        gr.HTML("""
        <div style="text-align:center;padding:20px;background:linear-gradient(135deg,#667eea,#764ba2);border-radius:15px;margin-bottom:20px;">
            <h1 style="color:white;margin:0;font-size:2.5em;">🆘 Disaster Resource Connector</h1>
            <p style="color:#fff;opacity:0.9;margin-top:10px;">Find emergency resources, report missing persons, volunteer, and more</p>
        </div>
        <div style="background:linear-gradient(90deg,#ff416c,#ff4b2b);color:white;padding:12px;border-radius:10px;text-align:center;margin-bottom:20px;">
            <strong>🚨 EMERGENCY:</strong> 112 | 🚔 Police: 100 | 🚑 Ambulance: 102/108 | 🚒 Fire: 101 | 🌊 NDMA: 1078
        </div>
        """)
        
        # Location Bar
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Row():
                    latitude = gr.Number(label="Latitude", precision=6)
                    longitude = gr.Number(label="Longitude", precision=6)
                location_status = gr.HTML("<span style='color:#666;'>👆 Click to detect location</span>")
                get_loc_btn = gr.Button("📍 Detect My Location", variant="secondary")
            with gr.Column(scale=1):
                lang_dropdown = gr.Dropdown(choices=[("English", "en"), ("हिंदी", "hi"), ("मराठी", "mr"), ("தமிழ்", "ta")], value="en", label="🌐 Language")
        
        # Main Tabs
        with gr.Tabs():
            # TAB 1: Find Resources
            with gr.Tab("🔍 Find Resources"):
                with gr.Row():
                    with gr.Column(scale=1):
                        message_input = gr.Textbox(label="What do you need?", placeholder="E.g., I need shelter and food", lines=3)
                        submit_btn = gr.Button("🔍 Find Resources", variant="primary", size="lg")
                        gr.HTML("<h4>⚡ Quick Actions</h4>")
                        with gr.Row():
                            shelter_btn = gr.Button("🏠 Shelter")
                            food_btn = gr.Button("🍲 Food")
                        with gr.Row():
                            medical_btn = gr.Button("🏥 Medical")
                            govt_btn = gr.Button("📋 Govt Aid")
                    with gr.Column(scale=2):
                        map_output = gr.HTML(create_map(None, None))
                response_output = gr.Markdown("👋 Detect your location and search for resources!")
            
            # TAB 2: SOS & Safety
            with gr.Tab("🆘 SOS & Safety"):
                with gr.Row():
                    with gr.Column():
                        gr.HTML("<h3>🆘 Send SOS Alert</h3>")
                        sos_name = gr.Textbox(label="Your Name")
                        sos_phone = gr.Textbox(label="Phone Number")
                        sos_type = gr.Dropdown(choices=["Medical Emergency", "Trapped", "Fire", "Flood", "Other"], label="Emergency Type")
                        sos_message = gr.Textbox(label="Describe your emergency", lines=2)
                        sos_btn = gr.Button("🆘 SEND SOS ALERT", variant="stop", size="lg")
                        sos_result = gr.Markdown()
                    with gr.Column():
                        gr.HTML("<h3>✅ Report I'm Safe</h3>")
                        safe_name = gr.Textbox(label="Your Name")
                        safe_phone = gr.Textbox(label="Phone Number")
                        safe_location = gr.Textbox(label="Current Location")
                        safe_message = gr.Textbox(label="Message to family")
                        safe_btn = gr.Button("✅ Report I'm Safe", variant="primary")
                        safe_result = gr.Markdown()
                gr.HTML("<hr>")
                gr.HTML("<h3>🔍 Search Safe Reports</h3>")
                with gr.Row():
                    search_safe_name = gr.Textbox(label="Name")
                    search_safe_phone = gr.Textbox(label="Phone")
                    search_safe_btn = gr.Button("Search")
                safe_search_result = gr.Markdown()
            
            # TAB 3: Weather
            with gr.Tab("🌤️ Weather"):
                weather_btn = gr.Button("🌤️ Get Weather & Alerts", variant="primary")
                weather_output = gr.Markdown("Click the button to get weather for your location")
            
            # TAB 4: Blood Banks
            with gr.Tab("🩸 Blood Banks"):
                blood_btn = gr.Button("🩸 Find Blood Banks", variant="primary")
                blood_output = gr.Markdown()
                blood_map = gr.HTML()
            
            # TAB 5: Missing Persons
            with gr.Tab("👤 Missing Persons"):
                with gr.Row():
                    with gr.Column():
                        gr.HTML("<h3>📝 Report Missing Person</h3>")
                        mp_name = gr.Textbox(label="Full Name*")
                        with gr.Row():
                            mp_age = gr.Number(label="Age", precision=0)
                            mp_gender = gr.Dropdown(choices=["Male", "Female", "Other"], label="Gender")
                        mp_description = gr.Textbox(label="Physical Description", lines=2)
                        mp_last_location = gr.Textbox(label="Last Seen Location")
                        mp_last_time = gr.Textbox(label="Last Seen Time")
                        mp_contact_name = gr.Textbox(label="Your Name")
                        mp_contact_phone = gr.Textbox(label="Your Phone*")
                        mp_submit = gr.Button("📝 Report Missing Person", variant="primary")
                        mp_result = gr.Markdown()
                    with gr.Column():
                        gr.HTML("<h3>🔍 Search Missing Persons</h3>")
                        mp_search_query = gr.Textbox(label="Search by name or location")
                        mp_search_btn = gr.Button("🔍 Search")
                        mp_search_result = gr.Markdown()
            
            # TAB 6: Volunteer
            with gr.Tab("🤝 Volunteer"):
                with gr.Row():
                    with gr.Column():
                        gr.HTML("<h3>📝 Register as Volunteer</h3>")
                        vol_name = gr.Textbox(label="Full Name*")
                        vol_phone = gr.Textbox(label="Phone*")
                        vol_email = gr.Textbox(label="Email")
                        vol_skills = gr.Textbox(label="Skills (comma separated)", placeholder="First Aid, Driving, Cooking, etc.")
                        vol_areas = gr.Textbox(label="Available Areas")
                        vol_availability = gr.Dropdown(choices=["Full-time", "Weekends", "Evenings", "On-call"], label="Availability")
                        vol_vehicle = gr.Checkbox(label="I have a vehicle")
                        vol_submit = gr.Button("📝 Register as Volunteer", variant="primary")
                        vol_result = gr.Markdown()
                    with gr.Column():
                        gr.HTML("<h3>📋 View Resource Requests</h3>")
                        view_req_btn = gr.Button("📋 View Pending Requests")
                        requests_output = gr.Markdown()
            
            # TAB 7: Request Help
            with gr.Tab("📋 Request Help"):
                gr.HTML("<h3>🙋 Request Resources</h3>")
                with gr.Row():
                    req_name = gr.Textbox(label="Your Name*")
                    req_phone = gr.Textbox(label="Phone*")
                with gr.Row():
                    req_type = gr.Dropdown(choices=["Food", "Water", "Medicine", "Clothes", "Shelter", "Rescue", "Medical", "Other"], label="Resource Type")
                    req_urgency = gr.Dropdown(choices=["critical", "high", "medium", "low"], label="Urgency")
                    req_quantity = gr.Number(label="Quantity", value=1, precision=0)
                req_description = gr.Textbox(label="Description", lines=2)
                req_location = gr.Textbox(label="Delivery Location")
                req_submit = gr.Button("📋 Submit Request", variant="primary")
                req_result = gr.Markdown()
            
            # TAB 8: Donate
            with gr.Tab("🎁 Donate"):
                gr.HTML("<h3>🎁 Donate Resources</h3>")
                with gr.Row():
                    don_name = gr.Textbox(label="Your Name*")
                    don_phone = gr.Textbox(label="Phone*")
                don_type = gr.Dropdown(choices=["Food", "Clothes", "Medicine", "Money", "Blood", "Other"], label="Donation Type")
                don_items = gr.Textbox(label="Items Description")
                don_quantity = gr.Textbox(label="Quantity")
                don_location = gr.Textbox(label="Pickup Location")
                don_submit = gr.Button("🎁 Register Donation", variant="primary")
                don_result = gr.Markdown()
            
            # TAB 9: Preparedness
            with gr.Tab("📚 Preparedness"):
                disaster_type = gr.Dropdown(choices=[("General Emergency", "general"), ("Flood", "flood"), ("Earthquake", "earthquake"), ("Cyclone", "cyclone")], value="general", label="Select Disaster Type")
                prep_btn = gr.Button("📋 Get Preparedness Guide", variant="primary")
                prep_output = gr.Markdown()
        
        # Footer
        gr.HTML("""<div style="text-align:center;padding:20px;margin-top:20px;color:#888;border-top:1px solid #eee;">
            <p>🆘 Disaster Resource Connector | 🇮🇳 Made for India | Data from verified sources</p>
        </div>""")
        
        # JavaScript for geolocation
        geo_js = """async function(){return new Promise((r)=>{if(navigator.geolocation){navigator.geolocation.getCurrentPosition((p)=>{r([p.coords.latitude,p.coords.longitude,"<span style='color:#10b981;'>✅ Location detected!</span>"]);},()=>{r([null,null,"<span style='color:#ef4444;'>❌ Location access denied</span>"]);},{enableHighAccuracy:true,timeout:15000});}else{r([null,null,"<span style='color:#ef4444;'>❌ Geolocation not supported</span>"]);}})}"""
        
        # Event Handlers
        get_loc_btn.click(None, [], [latitude, longitude, location_status], js=geo_js).then(lambda lat, lon: create_map(lat, lon), [latitude, longitude], [map_output])
        submit_btn.click(process_request, [message_input, latitude, longitude], [response_output, map_output])
        message_input.submit(process_request, [message_input, latitude, longitude], [response_output, map_output])
        
        shelter_btn.click(lambda lat, lon: process_request("I need emergency shelter", lat, lon), [latitude, longitude], [response_output, map_output])
        food_btn.click(lambda lat, lon: process_request("I need food and water", lat, lon), [latitude, longitude], [response_output, map_output])
        medical_btn.click(lambda lat, lon: process_request("I need medical help and hospitals", lat, lon), [latitude, longitude], [response_output, map_output])
        govt_btn.click(lambda lat, lon: process_request("Government disaster assistance", lat, lon), [latitude, longitude], [response_output, map_output])
        
        weather_btn.click(get_weather_display, [latitude, longitude], [weather_output])
        blood_btn.click(get_blood_banks_display, [latitude, longitude], [blood_output, blood_map])
        prep_btn.click(get_preparedness_display, [disaster_type], [prep_output])
        
        sos_btn.click(send_sos, [sos_name, sos_phone, sos_type, sos_message, latitude, longitude], [sos_result])
        safe_btn.click(report_safe_status, [safe_name, safe_phone, safe_location, safe_message, latitude, longitude], [safe_result])
        search_safe_btn.click(search_safe, [search_safe_name, search_safe_phone], [safe_search_result])
        
        mp_submit.click(report_missing, [mp_name, mp_age, mp_gender, mp_description, mp_last_location, mp_last_time, mp_contact_name, mp_contact_phone, latitude, longitude], [mp_result])
        mp_search_btn.click(search_missing, [mp_search_query], [mp_search_result])
        
        vol_submit.click(register_vol, [vol_name, vol_phone, vol_email, vol_skills, vol_areas, vol_availability, vol_vehicle, latitude, longitude], [vol_result])
        view_req_btn.click(view_requests, [], [requests_output])
        
        req_submit.click(create_request, [req_name, req_phone, req_type, req_description, req_urgency, req_quantity, req_location, latitude, longitude], [req_result])
        don_submit.click(register_donation, [don_name, don_phone, don_type, don_items, don_quantity, don_location, latitude, longitude], [don_result])
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)
