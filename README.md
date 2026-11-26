# 🏛️ FixMyCampus — Smart Campus Facilities & Maintenance System

> **A centralized, production-grade SaaS web platform where university students report campus maintenance issues and facilities administration efficiently tracks, dispatches technicians, and resolves them.**

Built with **100% Python** (**FastAPI**, **Pandas**, **NumPy**, **Matplotlib**), modern responsive CSS, and interactive client workflows.

---

## 🌟 Key Modules & Architecture

### 1. 🎓 Student & Campus Resident Portal (`/`)
- **Photographic Feed:** 2x2 grid of authentic campus maintenance issues with priority pills, status tags, and upvote counters.
- **Instant Search & Building Selector:** Filter problems by campus hall, category, and urgency.
- **"Me Too" Endorsements:** Students upvote open issues to increase priority and avoid duplicate spam.
- **Visual Modal Reporting:** Clean ticket submission modal with category, building, location detail, priority, description, and optional photo attachment.

### 2. 🎫 Ticket Detail & Lifecycle Stepper (`/ticket/{id}`)
- **4-Stage Progress Stepper:** `Reported` ➔ `Assigned` ➔ `In Progress` ➔ `Resolved`.
- **SLA Countdown & Overdue Badges:** Dynamic time computation based on priority level.
- **Resolution Proof & Feedback:** Students can rate resolved tickets (1-5 stars) and submit satisfaction notes.

### 3. 🛡️ Facilities Admin Command Center (`/admin`)
- **5 Executive KPI Cards:** Total Reported, Open Needs Action, Active In Progress, Overdue Breaches, and SLA Compliance Rate.
- **Staff Dispatch & Capacity Hub:** Roster view showing technician active workload (`Available`, `Normal`, `High Load`) and unassigned tickets count.
- **Interactive Master Grid:** Instant keyword search, status filter chips (`All`, `Urgent & Overdue`, `Unassigned`, `In Progress`, `Resolved`), and inline technician assignment dropdowns.
- **Live Matplotlib Analytics:**
  - *Issues by Category* (Donut Chart)
  - *Incident Hotspots by Building* (Horizontal Bar Chart)
  - *Weekly Inflow vs. Resolution Velocity* (Trend Chart)
- **1-Click CSV Export:** Generates downloadable Excel/CSV reports for facilities audits.

### 4. 📊 Data Science & Analytics Pipeline (`analytics_pipeline.py`)
- Independent analytical pipeline utilizing **Pandas** (cleaning, median imputation, categorical grouping), **NumPy** (vectorization, standard deviation, percentile benchmarks P50/P75/P90, boolean masking), and **Matplotlib** (3-panel performance dashboard).

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Install dependencies:
```bash
pip install fastapi uvicorn jinja2 python-multipart pandas numpy matplotlib pillow
```

### Launch the Application
```bash
python run.py
```
*Or directly via Uvicorn:*
```bash
uvicorn main:app --reload --port 8000
```
Open **`http://127.0.0.1:8000`** in your browser.

---

### Run Offline Analytics Pipeline
```bash
python analytics_pipeline.py
```
Generates statistical metrics in console and exports `campus_operations_report.png`.

---

### Automated Verification Test Suite
```bash
python test_app.py
```
Runs 10 end-to-end tests covering routes, forms, APIs, role switcher, and CSV exports.
