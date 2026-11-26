"""
Runner script for FixMyCampus.
Starts the Uvicorn web server on port 8000.
"""
import uvicorn

if __name__ == "__main__":
    print("\n=======================================================")
    print(" 🏛️  FIXMYCAMPUS — SMART CAMPUS PROBLEM REPORTING OS  ")
    print("=======================================================")
    print(" Server running at: http://127.0.0.1:8000")
    print(" Portals available:")
    print("   • Student Portal & Feed:  http://127.0.0.1:8000/")
    print("   • Admin Command Center:   http://127.0.0.1:8000/admin")
    print("   • Staff & Field Dispatch: http://127.0.0.1:8000/staff")
    print("   • Campus Notices:         http://127.0.0.1:8000/notices")
    print("=======================================================\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
