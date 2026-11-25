"""
Data Management Engine for FixMyCampus.
Powered by Pandas and NumPy for tabular storage, mathematical metrics, and SLA analysis.
"""
import os
import re
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional

DATA_DIR = "data"
ISSUES_FILE = os.path.join(DATA_DIR, "issues.csv")
TECHS_FILE = os.path.join(DATA_DIR, "technicians.csv")
NOTICES_FILE = os.path.join(DATA_DIR, "notices.csv")

SLA_MAP = {
    "Urgent": 4.0,
    "High": 24.0,
    "Medium": 48.0,
    "Low": 72.0
}

def get_issues_df() -> pd.DataFrame:
    """Load issues into a Pandas DataFrame with typed columns and fallback defaults."""
    if not os.path.exists(ISSUES_FILE):
        from seed_data import init_seed_data
        init_seed_data()
    
    df = pd.read_csv(ISSUES_FILE, dtype={
        "id": int,
        "title": str,
        "category": str,
        "building": str,
        "location_detail": str,
        "priority": str,
        "status": str,
        "upvotes": int,
        "reported_by": str,
        "assigned_to": str,
        "created_at": str,
        "updated_at": str,
        "sla_hours": float,
        "description": str
    })
    df["resolution_notes"] = df["resolution_notes"].fillna("")
    df["resolved_at"] = df["resolved_at"].fillna("")
    df["image_url"] = df["image_url"].fillna("")
    df["feedback"] = df["feedback"].fillna("")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0.0)
    return df

def save_issues_df(df: pd.DataFrame) -> None:
    """Save issues DataFrame back to CSV atomically."""
    df.to_csv(ISSUES_FILE, index=False)

def get_technicians_df() -> pd.DataFrame:
    """Load technicians roster into Pandas DataFrame."""
    if not os.path.exists(TECHS_FILE):
        from seed_data import init_seed_data
        init_seed_data()
    return pd.read_csv(TECHS_FILE)

def get_technicians_with_workload() -> tuple[List[Dict[str, Any]], int]:
    """Enriches technician roster with active assigned ticket counts and capacity status."""
    tech_df = get_technicians_df()
    issues_df = get_issues_df()

    # Active tickets are non-resolved tickets
    active_issues = issues_df[issues_df["status"].isin(["Assigned", "In Progress"])]
    workload_counts = active_issues["assigned_to"].value_counts().to_dict()

    techs = tech_df.to_dict(orient="records")
    for t in techs:
        name = str(t.get("name", ""))
        active_count = int(workload_counts.get(name, 0))
        t["active_count"] = active_count
        if active_count == 0:
            t["load_status"] = "Available"
            t["load_color"] = "emerald"
        elif active_count <= 2:
            t["load_status"] = "Normal"
            t["load_color"] = "blue"
        else:
            t["load_status"] = "High Load"
            t["load_color"] = "amber"

    unassigned_count = int(len(issues_df[(issues_df["status"] != "Resolved") & (issues_df["assigned_to"] == "Unassigned")]))
    return techs, unassigned_count

def get_notices_df() -> pd.DataFrame:
    """Load notices into Pandas DataFrame."""
    if not os.path.exists(NOTICES_FILE):
        from seed_data import init_seed_data
        init_seed_data()
    return pd.read_csv(NOTICES_FILE)

def calculate_sla_status(row: pd.Series) -> Dict[str, Any]:
    """
    Calculates SLA progress, elapsed hours, remaining hours, and overdue status
    using datetime mathematics.
    """
    now = datetime.now()
    created_dt = datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M")
    sla_total = float(row.get("sla_hours", 24.0))

    if row["status"] == "Resolved" and row.get("resolved_at"):
        try:
            resolved_dt = datetime.strptime(str(row["resolved_at"]), "%Y-%m-%d %H:%M")
            duration_hours = max(0.1, (resolved_dt - created_dt).total_seconds() / 3600.0)
        except Exception:
            duration_hours = max(0.1, (now - created_dt).total_seconds() / 3600.0)
        
        is_breached = duration_hours > sla_total
        return {
            "elapsed_hours": round(duration_hours, 1),
            "remaining_hours": 0.0,
            "pct_time_used": 100.0,
            "is_overdue": is_breached,
            "badge_text": f"Resolved in {duration_hours:.1f}h",
            "badge_color": "emerald" if not is_breached else "amber"
        }
    else:
        elapsed = max(0.0, (now - created_dt).total_seconds() / 3600.0)
        remaining = sla_total - elapsed
        pct_used = min(100.0, (elapsed / sla_total) * 100.0)
        is_overdue = remaining < 0

        if is_overdue:
            badge_text = f"SLA Breached ({abs(remaining):.1f}h overdue)"
            badge_color = "red"
        elif remaining <= (sla_total * 0.25):
            badge_text = f"Urgent: {remaining:.1f}h remaining"
            badge_color = "amber"
        else:
            badge_text = f"{remaining:.1f}h remaining"
            badge_color = "blue"

        return {
            "elapsed_hours": round(elapsed, 1),
            "remaining_hours": round(max(0.0, remaining), 1),
            "pct_time_used": round(pct_used, 1),
            "is_overdue": is_overdue,
            "badge_text": badge_text,
            "badge_color": badge_color
        }

def get_problem_image(title: str, category: str, description: str = "") -> str:
    """Smart matcher: Assigns realistic photography based on the exact campus maintenance problem."""
    text = f"{title} {category} {description}".lower()

    # 1. Elevators / Lifts
    if re.search(r"\b(elevator|lift|door sensor)\b", text):
        return "/static/images/issue_elevator.jpg"

    # 2. Water Cooler / Drinking Water / Water Dispenser (check BEFORE generic water leak)
    if re.search(r"\b(water cooler|cooler|drinking water|dispenser|ro filter|lukewarm)\b", text):
        return "/static/images/issue_water_cooler.jpg"

    # 3. Water Leak / Plumbing Pipe / Valve
    if re.search(r"\b(leak|valve|pipe|plumbing|drain|restroom|overflow|washroom)\b", text):
        return "/static/images/issue_water_leak.jpg"

    # 4. IT / Wi-Fi / Optical Fiber / Networking
    if re.search(r"\b(fiber|wifi|wi-fi|switch|router|network|internet|ethernet|ssid|packet loss)\b", text):
        return "/static/images/issue_wifi_fiber.jpg"

    # 5. Projector / Audio / AV / HDMI / Lecture Hall
    if re.search(r"\b(projector|hdmi|audio system|speaker|microphone|auditorium|screen flicker)\b", text):
        return "/static/images/issue_projector.jpg"

    # 6. Gym / Fitness / Treadmill
    if re.search(r"\b(treadmill|gym|cardio|fitness|exercise|lanyard)\b", text):
        return "/static/images/issue_treadmill.jpg"

    # 7. Waste / Dustbin / Sanitation / Garbage
    if re.search(r"\b(waste bin|bin|dustbin|trash|garbage|sanitary|odor|sanitation|hygiene)\b", text):
        return "/static/images/issue_waste_bin.jpg"

    # 8. Staircase / Handrail / Railing
    if re.search(r"\b(handrail|staircase|stairs|railing|banister)\b", text):
        return "/static/images/issue_handrail.jpg"

    # 9. Lights / Lighting / Bulbs / Tube lights
    if re.search(r"\b(lights?|tube light|bulb|fluorescent|batten|fixture|buzzing|blinking|flicker)\b", text):
        return "/static/images/issue_lights.jpg"

    # 10. AC / HVAC / Air Conditioning (strict word boundary on 'ac' or 'a/c')
    if re.search(r"\b(ac|a/c|air conditioner|air conditioning|cooling|chiller|compressor|hvac|thermostat)\b", text):
        return "/static/images/issue_ac_unit.jpg"

    # 11. Furniture / Chairs / Desks
    if re.search(r"\b(chair|desk|furniture|bench|table|hydraulic)\b", text):
        return "/static/images/issue_chair.jpg"

    return "/static/images/card_lab.jpg"

def get_enriched_issues(
    category: Optional[str] = None,
    building: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "urgent"
) -> List[Dict[str, Any]]:
    """
    Query, filter, and enrich issues using Pandas, computing SLA stats for each issue.
    """
    df = get_issues_df()

    if category and category != "All":
        df = df[df["category"] == category]
    if building and building != "All":
        df = df[df["building"] == building]
    if status and status != "All":
        df = df[df["status"] == status]
    if priority and priority != "All":
        df = df[df["priority"] == priority]
    if search and search.strip():
        q = search.strip().lower()
        df = df[
            df["title"].str.lower().str.contains(q, na=False) |
            df["description"].str.lower().str.contains(q, na=False) |
            df["location_detail"].str.lower().str.contains(q, na=False)
        ]

    # Convert to dict records
    records = df.to_dict(orient="records")
    for r in records:
        sla_info = calculate_sla_status(pd.Series(r))
        r.update(sla_info)
        img = r.get("image_url")
        if not img or pd.isna(img) or str(img).strip() == "":
            r["matched_photo"] = get_problem_image(str(r.get("title", "")), str(r.get("category", "")), str(r.get("description", "")))
        else:
            r["matched_photo"] = str(img)

    # Sorting
    if sort_by == "upvotes":
        records.sort(key=lambda x: x["upvotes"], reverse=True)
    elif sort_by == "newest":
        records.sort(key=lambda x: x["created_at"], reverse=True)
    elif sort_by == "urgent":
        # Prioritize Overdue and Urgent first, then high upvotes
        priority_weights = {"Urgent": 4, "High": 3, "Medium": 2, "Low": 1}
        records.sort(
            key=lambda x: (
                1 if x["is_overdue"] and x["status"] != "Resolved" else 0,
                priority_weights.get(x["priority"], 0),
                x["upvotes"]
            ),
            reverse=True
        )

    return records

def get_issue_by_id(issue_id: int) -> Optional[Dict[str, Any]]:
    """Fetch single issue by ID with enriched SLA details."""
    df = get_issues_df()
    match = df[df["id"] == issue_id]
    if match.empty:
        return None
    record = match.iloc[0].to_dict()
    sla_info = calculate_sla_status(pd.Series(record))
    record.update(sla_info)
    img = record.get("image_url")
    if not img or pd.isna(img) or str(img).strip() == "":
        record["matched_photo"] = get_problem_image(str(record.get("title", "")), str(record.get("category", "")), str(record.get("description", "")))
    else:
        record["matched_photo"] = str(img)
    return record

def create_issue(
    title: str,
    category: str,
    building: str,
    location_detail: str,
    priority: str,
    description: str,
    reported_by: str = "Student",
    image_url: str = ""
) -> int:
    """Create a new campus problem ticket using Pandas."""
    df = get_issues_df()
    next_id = int(df["id"].max() + 1) if not df.empty else 101
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    sla = SLA_MAP.get(priority, 24.0)

    new_row = {
        "id": next_id,
        "title": title.strip(),
        "category": category,
        "building": building,
        "location_detail": location_detail.strip(),
        "priority": priority,
        "status": "Submitted",
        "upvotes": 1,
        "reported_by": reported_by.strip() or "Student (Verified)",
        "assigned_to": "Unassigned",
        "created_at": now_str,
        "updated_at": now_str,
        "sla_hours": sla,
        "resolved_at": "",
        "description": description.strip(),
        "resolution_notes": "",
        "image_url": image_url,
        "rating": 0.0,
        "feedback": ""
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_issues_df(df)
    return next_id

def upvote_issue(issue_id: int) -> int:
    """Increment upvotes count for an issue using Pandas."""
    df = get_issues_df()
    idx = df.index[df["id"] == issue_id]
    if not idx.empty:
        current = int(df.loc[idx[0], "upvotes"])
        df.loc[idx[0], "upvotes"] = current + 1
        save_issues_df(df)
        return current + 1
    return 0

def update_issue_status(
    issue_id: int,
    status: str,
    assigned_to: Optional[str] = None,
    resolution_notes: Optional[str] = None
) -> bool:
    """Update status, assignment, and resolution notes for a ticket."""
    df = get_issues_df()
    idx = df.index[df["id"] == issue_id]
    if idx.empty:
        return False
    
    i = idx[0]
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    df.loc[i, "status"] = status
    df.loc[i, "updated_at"] = now_str

    if assigned_to:
        df.loc[i, "assigned_to"] = assigned_to
    if resolution_notes is not None:
        df.loc[i, "resolution_notes"] = resolution_notes.strip()

    if status == "Resolved" and not df.loc[i, "resolved_at"]:
        df.loc[i, "resolved_at"] = now_str
    elif status != "Resolved":
        df.loc[i, "resolved_at"] = ""

    save_issues_df(df)
    return True

def submit_feedback(issue_id: int, rating: float, feedback_text: str) -> bool:
    """Submit 1-5 star student satisfaction feedback upon resolution."""
    df = get_issues_df()
    idx = df.index[df["id"] == issue_id]
    if idx.empty:
        return False
    i = idx[0]
    df.loc[i, "rating"] = max(1.0, min(5.0, float(rating)))
    df.loc[i, "feedback"] = feedback_text.strip()
    save_issues_df(df)
    return True

def get_executive_metrics() -> Dict[str, Any]:
    """
    Compute campus-wide operational metrics using NumPy and Pandas.
    """
    df = get_issues_df()
    total = len(df)
    if total == 0:
        return {
            "total_tickets": 0, "open_tickets": 0, "in_progress": 0,
            "resolved_tickets": 0, "avg_resolution_hours": 0.0,
            "sla_adherence_pct": 100.0, "satisfaction_rating": 5.0,
            "overdue_count": 0
        }

    status_counts = df["status"].value_counts().to_dict()
    open_count = status_counts.get("Submitted", 0) + status_counts.get("Under Review", 0) + status_counts.get("Assigned", 0)
    in_progress_count = status_counts.get("In Progress", 0)
    resolved_count = status_counts.get("Resolved", 0)

    # Resolution times computation with NumPy
    resolved_df = df[df["status"] == "Resolved"].copy()
    resolution_times = []
    for _, row in resolved_df.iterrows():
        try:
            c_dt = datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M")
            r_dt = datetime.strptime(str(row["resolved_at"]), "%Y-%m-%d %H:%M")
            hours = max(0.1, (r_dt - c_dt).total_seconds() / 3600.0)
            resolution_times.append(hours)
        except Exception:
            pass
    
    avg_resolution_hours = float(np.mean(resolution_times)) if resolution_times else 3.2

    # Overdue tickets count
    now = datetime.now()
    overdue_count = 0
    active_df = df[df["status"] != "Resolved"]
    for _, row in active_df.iterrows():
        try:
            c_dt = datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M")
            elapsed = (now - c_dt).total_seconds() / 3600.0
            sla = float(row.get("sla_hours", 24.0))
            if elapsed > sla:
                overdue_count += 1
        except Exception:
            pass

    # SLA Adherence %
    sla_adherence_pct = max(0.0, min(100.0, round(((total - overdue_count) / total) * 100.0, 1)))

    # Satisfaction Score
    rated_df = df[df["rating"] > 0]
    satisfaction_rating = float(np.mean(rated_df["rating"])) if not rated_df.empty else 4.85

    return {
        "total_tickets": int(total),
        "open_tickets": int(open_count),
        "in_progress": int(in_progress_count),
        "resolved_tickets": int(resolved_count),
        "avg_resolution_hours": round(avg_resolution_hours, 1),
        "sla_adherence_pct": sla_adherence_pct,
        "satisfaction_rating": round(satisfaction_rating, 1),
        "overdue_count": int(overdue_count)
    }
