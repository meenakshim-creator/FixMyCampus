"""
FixMyCampus — Smart Campus Problem Reporting & Management System.
FastAPI Web Application with Pure Python Backend & Semantic Zero-JavaScript Frontend.
"""
import os
import shutil
from typing import Optional
from fastapi import FastAPI, Request, Form, File, UploadFile, Query
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import data_manager
import analytics

app = FastAPI(title="FixMyCampus", description="Smart Campus Problem Reporting & Management System")

# Ensure required directories exist
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("data", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Helper to retrieve active role from cookies (default: student)
def get_user_role(request: Request) -> str:
    role = request.cookies.get("active_role", "student").lower()
    return role if role in ["student", "admin", "staff"] else "student"

CAMPUS_BUILDINGS = [
    "Central Library",
    "Science Block A",
    "Engineering Block B",
    "Admin Complex",
    "Girls Hostel 2",
    "Boys Hostel 1",
    "Cafeteria & Dining",
    "Sports Arena"
]

CATEGORIES = [
    {"name": "Electrical", "desc": "Power, wiring, switches, lighting"},
    {"name": "Plumbing", "desc": "Leaks, pipes, drainage, washrooms"},
    {"name": "IT & WiFi", "desc": "Network, routers, switches, fiber"},
    {"name": "HVAC & Cooling", "desc": "Air conditioners, fans, ventilation"},
    {"name": "Sanitation", "desc": "Cleanliness, waste disposal, hygiene"},
    {"name": "Labs & Equipment", "desc": "Projectors, computers, lab gear"},
    {"name": "Civil & Furniture", "desc": "Doors, desks, windows, masonry"}
]

@app.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    category: Optional[str] = Query("All"),
    building: Optional[str] = Query("All"),
    status: Optional[str] = Query("All"),
    priority: Optional[str] = Query("All"),
    search: Optional[str] = Query(None),
    sort: Optional[str] = Query("urgent"),
    msg: Optional[str] = Query(None)
):
    role = get_user_role(request)
    issues = data_manager.get_enriched_issues(
        category=category,
        building=building,
        status=status,
        priority=priority,
        search=search,
        sort_by=sort
    )
    metrics = data_manager.get_executive_metrics()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "role": role,
            "issues": issues,
            "metrics": metrics,
            "categories": CATEGORIES,
            "buildings": CAMPUS_BUILDINGS,
            "selected_category": category,
            "selected_building": building,
            "selected_status": status,
            "selected_priority": priority,
            "search_query": search or "",
            "selected_sort": sort,
            "flash_message": msg
        }
    )

@app.post("/report")
async def report_issue(
    request: Request,
    title: str = Form(...),
    category: str = Form(...),
    building: str = Form(...),
    location_detail: str = Form(...),
    priority: str = Form(...),
    description: str = Form(...),
    reported_by: Optional[str] = Form("Student (Verified)"),
    photo: Optional[UploadFile] = File(None)
):
    image_url = ""
    if photo and photo.filename:
        safe_name = f"issue_{os.path.basename(photo.filename)}"
        target_path = os.path.join("static", "uploads", safe_name)
        with open(target_path, "wb") as f:
            shutil.copyfileobj(photo.file, f)
        image_url = f"/static/uploads/{safe_name}"

    new_id = data_manager.create_issue(
        title=title,
        category=category,
        building=building,
        location_detail=location_detail,
        priority=priority,
        description=description,
        reported_by=reported_by or "Student (Verified)",
        image_url=image_url
    )
    return RedirectResponse(
        url=f"/ticket/{new_id}?msg=Ticket%20%23{new_id}%20successfully%20submitted%20to%20facilities%20desk!",
        status_code=303
    )

@app.post("/upvote/{issue_id}")
async def upvote_issue(issue_id: int, request: Request, redirect_to: Optional[str] = Form("/")):
    data_manager.upvote_issue(issue_id)
    dest = redirect_to or "/"
    return RedirectResponse(url=f"{dest}?msg=Thanks!%20Your%20%27Me%20Too%27%20endorsement%20raised%20this%20ticket%27s%20urgency.", status_code=303)

@app.post("/api/upvote/{issue_id}")
async def api_upvote(issue_id: int):
    new_count = data_manager.upvote_issue(issue_id)
    return {"success": True, "upvotes": new_count, "issue_id": issue_id}


@app.get("/ticket/{issue_id}", response_class=HTMLResponse)
async def ticket_detail(issue_id: int, request: Request, msg: Optional[str] = Query(None)):
    role = get_user_role(request)
    issue = data_manager.get_issue_by_id(issue_id)
    if not issue:
        return RedirectResponse(url="/?msg=Ticket%20not%20found", status_code=303)

    technicians = data_manager.get_technicians_df().to_dict(orient="records")

    return templates.TemplateResponse(
        request=request,
        name="ticket_detail.html",
        context={
            "role": role,
            "issue": issue,
            "technicians": technicians,
            "flash_message": msg
        }
    )

@app.post("/ticket/{issue_id}/update-status")
async def update_status(
    issue_id: int,
    request: Request,
    status: str = Form(...),
    assigned_to: Optional[str] = Form(None),
    resolution_notes: Optional[str] = Form(None),
    redirect_to: Optional[str] = Form(None)
):
    data_manager.update_issue_status(
        issue_id=issue_id,
        status=status,
        assigned_to=assigned_to,
        resolution_notes=resolution_notes
    )
    dest = redirect_to or f"/ticket/{issue_id}"
    return RedirectResponse(url=f"{dest}?msg=Ticket%20%23{issue_id}%20updated%20to%20{status}!", status_code=303)

@app.post("/ticket/{issue_id}/feedback")
async def give_feedback(
    issue_id: int,
    rating: float = Form(...),
    feedback: str = Form(...)
):
    data_manager.submit_feedback(issue_id, rating, feedback)
    return RedirectResponse(url=f"/ticket/{issue_id}?msg=Thank%20you%20for%20your%20satisfaction%20feedback!", status_code=303)

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    category: Optional[str] = Query("All"),
    status: Optional[str] = Query("All"),
    priority: Optional[str] = Query("All"),
    search: Optional[str] = Query(None),
    msg: Optional[str] = Query(None)
):
    metrics = data_manager.get_executive_metrics()
    issues = data_manager.get_enriched_issues(
        category=category,
        status=status,
        priority=priority,
        search=search,
        sort_by="urgent"
    )
    charts = analytics.get_all_analytics_charts()
    technicians, unassigned_count = data_manager.get_technicians_with_workload()

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "role": "admin",
            "metrics": metrics,
            "issues": issues,
            "charts": charts,
            "technicians": technicians,
            "unassigned_count": unassigned_count,
            "categories": CATEGORIES,
            "selected_category": category,
            "selected_status": status,
            "selected_priority": priority,
            "search_query": search or "",
            "flash_message": msg
        }
    )

@app.get("/admin/export-csv")
async def export_csv():
    df = data_manager.get_issues_df()
    csv_data = df.to_csv(index=False)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=FixMyCampus_Report.csv"}
    )

@app.get("/staff", response_class=HTMLResponse)
async def staff_portal(
    request: Request,
    tech_name: Optional[str] = Query("Rajesh Kumar"),
    msg: Optional[str] = Query(None)
):
    technicians = data_manager.get_technicians_df().to_dict(orient="records")
    all_issues = data_manager.get_enriched_issues()

    # Filter for currently selected technician or unassigned
    tech_issues = [i for i in all_issues if tech_name.lower() in i.get("assigned_to", "").lower()]
    unassigned = [i for i in all_issues if i.get("status") in ["Submitted", "Under Review"] or i.get("assigned_to") == "Unassigned"]

    return templates.TemplateResponse(
        request=request,
        name="staff.html",
        context={
            "role": "staff",
            "technicians": technicians,
            "selected_tech": tech_name,
            "assigned_issues": tech_issues,
            "unassigned_issues": unassigned,
            "flash_message": msg
        }
    )

@app.get("/notices", response_class=HTMLResponse)
async def campus_notices(request: Request):
    role = get_user_role(request)
    notices = data_manager.get_notices_df().to_dict(orient="records")
    return templates.TemplateResponse(
        request=request,
        name="notices.html",
        context={
            "role": role,
            "notices": notices
        }
    )

@app.get("/switch-role")
async def switch_role(role: str, redirect_to: Optional[str] = "/"):
    safe_role = role.lower() if role.lower() in ["student", "admin", "staff"] else "student"
    target = redirect_to or "/"
    if safe_role == "admin" and target == "/":
        target = "/admin"
    elif safe_role == "staff" and target == "/":
        target = "/staff"
    elif safe_role == "student" and target in ["/admin", "/staff"]:
        target = "/"

    response = RedirectResponse(url=target, status_code=303)
    response.set_cookie(key="active_role", value=safe_role, max_age=86400*30, path="/")
    return response
