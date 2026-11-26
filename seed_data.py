"""
Seed dataset generator for FixMyCampus.
Generates realistic, rich initial campus issues and technician rosters using Pandas.
"""
import os
import pandas as pd
from datetime import datetime, timedelta

def init_seed_data():
    os.makedirs("data", exist_ok=True)
    os.makedirs("static/css", exist_ok=True)
    os.makedirs("static/uploads", exist_ok=True)
    os.makedirs("templates", exist_ok=True)

    now = datetime.now()

    # Technicians dataset
    technicians = [
        {"id": 1, "name": "Rajesh Kumar", "role": "Senior Electrician", "dept": "Electrical", "phone": "+91 98765-43210", "rating": 4.9, "status": "On Duty"},
        {"id": 2, "name": "Suresh Patel", "role": "Lead Plumber & Piping", "dept": "Plumbing", "phone": "+91 98765-43211", "rating": 4.8, "status": "On Duty"},
        {"id": 3, "name": "Vikramaditya Roy", "role": "Campus Network Engineer", "dept": "IT & WiFi", "phone": "+91 98765-43212", "rating": 4.95, "status": "On Duty"},
        {"id": 4, "name": "Anita Sen", "role": "Sanitation & Housekeeping Lead", "dept": "Sanitation", "phone": "+91 98765-43213", "rating": 4.7, "status": "On Duty"},
        {"id": 5, "name": "Manoj Sharma", "role": "HVAC / AC Specialist", "dept": "HVAC & Cooling", "phone": "+91 98765-43214", "rating": 4.85, "status": "On Duty"},
        {"id": 6, "name": "Harish Verma", "role": "Civil & Carpentry Contractor", "dept": "Civil & Furniture", "phone": "+91 98765-43215", "rating": 4.65, "status": "Available"}
    ]
    pd.DataFrame(technicians).to_csv("data/technicians.csv", index=False)

    # Campus maintenance issues dataset
    issues = [
        {
            "id": 101,
            "title": "Core Optical Fiber Switch Flapping — WiFi Down",
            "category": "IT & WiFi",
            "building": "Central Library",
            "location_detail": "2nd Floor Digital Study Hall",
            "priority": "Urgent",
            "status": "In Progress",
            "upvotes": 47,
            "reported_by": "Aarav Sharma (CS-24)",
            "assigned_to": "Vikramaditya Roy",
            "created_at": (now - timedelta(hours=3, minutes=20)).strftime("%Y-%m-%d %H:%M"),
            "updated_at": (now - timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M"),
            "sla_hours": 4.0,
            "resolved_at": "",
            "description": "High packet loss and random SSID disconnects affecting more than 60 students in the digital research section.",
            "resolution_notes": "Identified bent patch cable in rack B3; replacing with Cat6A shielded cable now.",
            "image_url": "",
            "rating": 0.0,
            "feedback": ""
        },
        {
            "id": 102,
            "title": "Severe Main Water Inflow Valve Leakage",
            "category": "Plumbing",
            "building": "Girls Hostel 2",
            "location_detail": "Ground Floor Restroom Wing C",
            "priority": "Urgent",
            "status": "In Progress",
            "upvotes": 34,
            "reported_by": "Neha Patel (BT-23)",
            "assigned_to": "Suresh Patel",
            "created_at": (now - timedelta(hours=4, minutes=10)).strftime("%Y-%m-%d %H:%M"),
            "updated_at": (now - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M"),
            "sla_hours": 4.0,
            "resolved_at": "",
            "description": "Water pressure overflowing onto the walkway outside rooms G-04 through G-08. Slip hazard for residents.",
            "resolution_notes": "Main intake shut off temporarily; installing heavy-duty stainless steel brass ball valve.",
            "image_url": "",
            "rating": 0.0,
            "feedback": ""
        },
        {
            "id": 103,
            "title": "Ceiling Projector & Audio System Flickering",
            "category": "Labs & Equipment",
            "building": "Engineering Block B",
            "location_detail": "Seminar Auditorium 301",
            "priority": "High",
            "status": "Assigned",
            "upvotes": 19,
            "reported_by": "Prof. R. Deshmukh",
            "assigned_to": "Rajesh Kumar",
            "created_at": (now - timedelta(hours=6, minutes=45)).strftime("%Y-%m-%d %H:%M"),
            "updated_at": (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            "sla_hours": 24.0,
            "resolved_at": "",
            "description": "HDMI signal cutting off every 4 minutes. Important guest faculty session scheduled tomorrow at 10 AM.",
            "resolution_notes": "Dispatched technician to check transmitter power supply.",
            "image_url": "",
            "rating": 0.0,
            "feedback": ""
        },
        {
            "id": 104,
            "title": "AC Compressor Tripping Circuit Breaker",
            "category": "HVAC & Cooling",
            "building": "Science Block A",
            "location_detail": "Room 204 — Molecular Biology Lab",
            "priority": "High",
            "status": "In Progress",
            "upvotes": 12,
            "reported_by": "Dr. Sunita Rao",
            "assigned_to": "Manoj Sharma",
            "created_at": (now - timedelta(hours=8, minutes=15)).strftime("%Y-%m-%d %H:%M"),
            "updated_at": (now - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"),
            "sla_hours": 24.0,
            "resolved_at": "",
            "description": "Temperature-sensitive reagents in incubators require stable 21C ambient temperature. AC trips every 30 minutes.",
            "resolution_notes": "Replaced thermal overload relay on outdoor compressor unit.",
            "image_url": "",
            "rating": 0.0,
            "feedback": ""
        },
        {
            "id": 105,
            "title": "Elevator #2 Stuck Between 3rd & 4th Floor Door Sensor Jam",
            "category": "Electrical",
            "building": "Admin Complex",
            "location_detail": "Central Lift Lobby",
            "priority": "Urgent",
            "status": "Resolved",
            "upvotes": 28,
            "reported_by": "Kavita Nair (Staff)",
            "assigned_to": "Rajesh Kumar",
            "created_at": (now - timedelta(hours=14)).strftime("%Y-%m-%d %H:%M"),
            "updated_at": (now - timedelta(hours=11)).strftime("%Y-%m-%d %H:%M"),
            "sla_hours": 4.0,
            "resolved_at": (now - timedelta(hours=11)).strftime("%Y-%m-%d %H:%M"),
            "description": "Lift door safety light curtain obstructed by misaligned sensor. Passengers helped out safely.",
            "resolution_notes": "Re-calibrated optical alignment curtain; safety test passed with 10 consecutive floor cycles.",
            "image_url": "",
            "rating": 5.0,
            "feedback": "Fixed in under 2 hours, excellent swift response by Rajesh!"
        },
        {
            "id": 106,
            "title": "Sanitary Waste Bin Overflowing & Odor",
            "category": "Sanitation",
            "building": "Boys Hostel 1",
            "location_detail": "2nd Floor West Wing Corridor",
            "priority": "Medium",
            "status": "Resolved",
            "upvotes": 15,
            "reported_by": "Rohan Gupta (ME-25)",
            "assigned_to": "Anita Sen",
            "created_at": (now - timedelta(hours=18)).strftime("%Y-%m-%d %H:%M"),
            "updated_at": (now - timedelta(hours=15)).strftime("%Y-%m-%d %H:%M"),
            "sla_hours": 48.0,
            "resolved_at": (now - timedelta(hours=15)).strftime("%Y-%m-%d %H:%M"),
            "description": "Waste bins not cleared since yesterday afternoon causing unpleasant odor in the corridor.",
            "resolution_notes": "Deep cleaned and sanitized corridor; replaced heavy-duty pedal bins.",
            "image_url": "",
            "rating": 5.0,
            "feedback": "Corridor is clean and fresh now. Thank you!"
        },
        {
            "id": 107,
            "title": "Broken Handrail on Fire Escape Staircase",
            "category": "Civil & Furniture",
            "building": "Engineering Block B",
            "location_detail": "South Staircase Level 2 to 3",
            "priority": "Medium",
            "status": "Under Review",
            "upvotes": 8,
            "reported_by": "Aniket Joshi (CV-24)",
            "assigned_to": "Harish Verma",
            "created_at": (now - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
            "updated_at": (now - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
            "sla_hours": 48.0,
            "resolved_at": "",
            "description": "Metal bracket holding the banister came loose. Could be unsafe during crowd movement.",
            "resolution_notes": "Civil inspection scheduled for afternoon shift.",
            "image_url": "",
            "rating": 0.0,
            "feedback": ""
        },
        {
            "id": 108,
            "title": "Water Cooler Dispensing Lukewarm / Murky Water",
            "category": "Plumbing",
            "building": "Cafeteria & Dining",
            "location_detail": "Main Food Court Exit",
            "priority": "High",
            "status": "Resolved",
            "upvotes": 22,
            "reported_by": "Priya Sen (MBA-24)",
            "assigned_to": "Suresh Patel",
            "created_at": (now - timedelta(hours=22)).strftime("%Y-%m-%d %H:%M"),
            "updated_at": (now - timedelta(hours=19)).strftime("%Y-%m-%d %H:%M"),
            "sla_hours": 24.0,
            "resolved_at": (now - timedelta(hours=19)).strftime("%Y-%m-%d %H:%M"),
            "description": "RO filter warning buzzer is beeping and water flow has dropped significantly.",
            "resolution_notes": "Flushed secondary sediment filter and installed new activated carbon cartridge.",
            "image_url": "",
            "rating": 4.8,
            "feedback": "Water is clear and chilled again!"
        },
        {
            "id": 109,
            "title": "Fluorescent Lights Buzzing and Blinking Constantly",
            "category": "Electrical",
            "building": "Central Library",
            "location_detail": "1st Floor Quiet Reading Zone",
            "priority": "Low",
            "status": "Submitted",
            "upvotes": 6,
            "reported_by": "Siddharth Jain (CS-26)",
            "assigned_to": "Unassigned",
            "created_at": (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            "updated_at": (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            "sla_hours": 72.0,
            "resolved_at": "",
            "description": "Two LED batten fixtures make a high-pitched buzzing noise distracting students studying for midterms.",
            "resolution_notes": "",
            "image_url": "",
            "rating": 0.0,
            "feedback": ""
        },
        {
            "id": 110,
            "title": "Gym Treadmill #3 Emergency Stop Button Loose",
            "category": "Labs & Equipment",
            "building": "Sports Arena",
            "location_detail": "Ground Floor Cardio Zone",
            "priority": "High",
            "status": "Assigned",
            "upvotes": 11,
            "reported_by": "Coach Virender",
            "assigned_to": "Harish Verma",
            "created_at": (now - timedelta(hours=9)).strftime("%Y-%m-%d %H:%M"),
            "updated_at": (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
            "sla_hours": 24.0,
            "resolved_at": "",
            "description": "The magnetic emergency lanyard clip does not cut power reliably when pulled.",
            "resolution_notes": "Treadmill unplugged with 'Out of Order' maintenance tag pending switch replacement.",
            "image_url": "",
            "rating": 0.0,
            "feedback": ""
        }
    ]
    pd.DataFrame(issues).to_csv("data/issues.csv", index=False)

    # Campus broadcast alerts
    notices = [
        {
            "id": 1,
            "title": "Scheduled Chilled Water Line Maintenance — Science Blocks A & B",
            "date": now.strftime("%b %d, %Y"),
            "priority": "Announcement",
            "department": "Facilities & HVAC",
            "message": "Routine chemical treatment and pipeline cleaning of the central chilled loop will occur this Saturday between 06:00 AM and 11:00 AM. AC ventilation will operate on fan-only mode during this window."
        },
        {
            "id": 2,
            "title": "Fiber Optic Redundancy Upgrade for Campus Hostels",
            "date": (now - timedelta(days=1)).strftime("%b %d, %Y"),
            "priority": "Network Advisory",
            "department": "Campus IT Services",
            "message": "New 10 Gbps redundant backhaul links have been successfully spliced and activated for Girls Hostel 1 & 2 and Boys Hostel 1. Peak hour streaming congestion resolved."
        },
        {
            "id": 3,
            "title": "Semi-Annual Fire Extinguisher & Alarm Testing",
            "date": (now - timedelta(days=3)).strftime("%b %d, %Y"),
            "priority": "Safety Drill",
            "department": "Safety & Disaster Management",
            "message": "All building fire wardens and lab technicians have completed hydro-testing of pressure vessels across engineering workshops."
        }
    ]
    pd.DataFrame(notices).to_csv("data/notices.csv", index=False)
    print("Seed data generated successfully.")

if __name__ == "__main__":
    init_seed_data()
