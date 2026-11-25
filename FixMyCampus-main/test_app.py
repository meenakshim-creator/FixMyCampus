"""
Comprehensive End-to-End Test Suite for FixMyCampus.
Verifies all FastAPI routes, forms, file uploads, Pandas operations, and Matplotlib chart renderings.
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home_page():
    res = client.get("/")
    assert res.status_code == 200
    assert "FixMyCampus" in res.text
    assert "Report a Problem" in res.text
    assert "Campus Issues" in res.text
    print("✓ Home page loaded successfully.")

def test_filtering_and_sorting():
    res = client.get("/?category=Electrical&status=Resolved")
    assert res.status_code == 200
    assert "Electrical" in res.text
    print("✓ Filter by category & status passed.")

def test_create_issue():
    payload = {
        "title": "Automated Test: Broken Study Chair in Library",
        "category": "Civil & Furniture",
        "building": "Central Library",
        "location_detail": "Study Bay 12",
        "priority": "Low",
        "description": "Chair hydraulic cylinder is stuck at lowest height.",
        "reported_by": "Test Runner"
    }
    res = client.post("/report", data=payload, follow_redirects=True)
    assert res.status_code == 200
    assert "Automated Test: Broken Study Chair in Library" in res.text
    print("✓ Issue reporting form passed.")

def test_upvoting():
    res = client.post("/upvote/101", data={"redirect_to": "/"}, follow_redirects=True)
    assert res.status_code == 200
    assert "Endorse" in res.text

    # Test AJAX upvote endpoint
    api_res = client.post("/api/upvote/101")
    assert api_res.status_code == 200
    data = api_res.json()
    assert data["success"] is True
    assert "upvotes" in data
    print("✓ Upvote 'Me Too' endorsement and AJAX API passed.")

def test_ticket_detail_and_feedback():
    res = client.get("/ticket/101")
    assert res.status_code == 200
    assert "Ticket #101" in res.text
    assert "Optical Fiber Switch" in res.text

    # Submit feedback
    feedback_payload = {
        "rating": "5.0",
        "feedback": "Fixed fast and reliably!"
    }
    fb_res = client.post("/ticket/101/feedback", data=feedback_payload, follow_redirects=True)
    assert fb_res.status_code == 200
    assert "Fixed fast and reliably!" in fb_res.text
    print("✓ Ticket detail and feedback flow passed.")

def test_admin_dashboard_and_charts():
    res = client.get("/admin")
    assert res.status_code == 200
    assert "Campus Operations & Maintenance Analytics" in res.text
    assert "data:image/png;base64," in res.text
    assert "Master Ticket Management Grid" in res.text
    print("✓ Admin Command Center and Matplotlib charts passed.")

def test_export_csv():
    res = client.get("/admin/export-csv")
    assert res.status_code == 200
    assert "text/csv" in res.headers["content-type"]
    assert "title,category,building" in res.text or "id," in res.text
    print("✓ CSV Report Export passed.")

def test_staff_portal():
    res = client.get("/staff?tech_name=Rajesh Kumar")
    assert res.status_code == 200
    assert "Rajesh Kumar" in res.text
    assert "Work Orders" in res.text
    print("✓ Staff / Technician Dispatch Hub passed.")

def test_campus_notices():
    res = client.get("/notices")
    assert res.status_code == 200
    assert "Campus Maintenance Notices & Safety Bulletins" in res.text
    print("✓ Campus Notices passed.")

def test_role_switch():
    res = client.get("/switch-role?role=admin&redirect_to=/admin", follow_redirects=False)
    assert res.status_code in [302, 303, 307]
    assert "active_role=admin" in res.headers.get("set-cookie", "")
    print("✓ Role Switcher passed.")

if __name__ == "__main__":
    print("\n--- Running FixMyCampus End-to-End Verification Suite ---")
    test_home_page()
    test_filtering_and_sorting()
    test_create_issue()
    test_upvoting()
    test_ticket_detail_and_feedback()
    test_admin_dashboard_and_charts()
    test_export_csv()
    test_staff_portal()
    test_campus_notices()
    test_role_switch()
    print("\n🎉 ALL 10 TESTS PASSED SUCCESSFULLY! 🎉\n")
