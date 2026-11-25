"""
=============================================================================
FixMyCampus — Facilities Operations & SLA Analytics Pipeline
Module: analytics_pipeline.py
Purpose: Batch operational metrics, SLA compliance evaluation & statistical reporting
Libraries: Pandas, NumPy, Matplotlib
=============================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# PART 1: PANDAS — Ingestion, Cleaning, Manipulation & Aggregation
# =============================================================================
print("=" * 65)
print("PART 1: PANDAS (Data Ingestion, Cleaning, Grouping & Sorting)")
print("=" * 65)

# Maintenance ticket dataset
raw_data = {
    "Ticket_ID": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    "Category": [
        "IT & WiFi", "Plumbing", "Labs & Equipment", "HVAC", 
        "Electrical", "Sanitation", "Civil", "Plumbing", 
        "Electrical", "Sports & Gym"
    ],
    "Building": [
        "Central Library", "Girls Hostel 2", "Engg Block B", "Science Block A", 
        "Admin Complex", "Boys Hostel 1", "Engg Block B", "Cafeteria", 
        "Central Library", "Sports Arena"
    ],
    "Priority": ["Urgent", "Urgent", "High", "High", "Urgent", "Medium", "Medium", "High", "Low", "High"],
    "Target_SLA_Hours": [4.0, 4.0, 24.0, 24.0, 4.0, 48.0, 48.0, 24.0, 72.0, 24.0],
    "Actual_Resolution_Hours": [3.1, 4.8, 18.5, 22.0, 2.7, 36.0, 42.5, 19.2, 58.0, 21.0],
    "Student_Upvotes": [77, 34, 19, 12, 28, 15, 8, 22, 6, 11],
    "Feedback_Rating": [5.0, 4.2, 4.5, 4.0, 4.8, 4.6, None, 4.7, 4.1, 4.4]  # Missing rating for imputation
}

# 1. Create DataFrame
df = pd.DataFrame(raw_data)

# 2. Data Cleaning: Impute missing ratings with column median
imputed_val = round(float(df["Feedback_Rating"].median()), 1)
df["Feedback_Rating"] = df["Feedback_Rating"].fillna(imputed_val)

# 3. Filtering: Query high-urgency unresolved or priority tickets
urgent_tickets = df[df["Priority"].isin(["Urgent", "High"])].copy()

# 4. GroupBy & Multi-column Aggregations
category_summary = df.groupby("Category").agg(
    Ticket_Count=("Ticket_ID", "count"),
    Avg_Resolution_Hours=("Actual_Resolution_Hours", "mean"),
    Total_Upvotes=("Student_Upvotes", "sum"),
    Avg_Rating=("Feedback_Rating", "mean")
).reset_index()

# 5. Sorting by student demand
category_summary = category_summary.sort_values(by="Total_Upvotes", ascending=False)

print("\n--- Summary by Maintenance Category (Grouped & Sorted by Upvotes) ---")
print(category_summary.to_string(index=False))


# =============================================================================
# PART 2: NUMPY — Mathematical Modeling, Vectorization & Statistical Metrics
# =============================================================================
print("\n" + "=" * 65)
print("PART 2: NUMPY (Vectorization, Mathematical Modeling & Statistics)")
print("=" * 65)

# Convert DataFrame columns into high-performance NumPy arrays
actual_hours = df["Actual_Resolution_Hours"].to_numpy()
target_hours = df["Target_SLA_Hours"].to_numpy()
ratings = df["Feedback_Rating"].to_numpy()
upvotes = df["Student_Upvotes"].to_numpy()

# 1. Conditional Vectorization using np.where
status_flags = np.where(actual_hours > target_hours, "BREACHED", "COMPLIANT")
df["SLA_Status"] = status_flags

# 2. Statistical Metrics: Mean, Standard Deviation and Variance
mean_res = np.mean(actual_hours)
std_res = np.std(actual_hours)
variance_res = np.var(actual_hours)

# 3. Percentiles (Median / 50th, 75th, and 90th percentile SLA benchmarks)
p50 = np.percentile(actual_hours, 50)
p75 = np.percentile(actual_hours, 75)
p90 = np.percentile(actual_hours, 90)

# 4. Boolean Masking & SLA Compliance Rate
breached_mask = (actual_hours > target_hours)
total_tickets = actual_hours.size
breached_tickets = np.count_nonzero(breached_mask)
compliance_rate = ((total_tickets - breached_tickets) / total_tickets) * 100.0

# 5. Weighted Average: Student Satisfaction weighted by ticket upvotes
weighted_rating = np.average(ratings, weights=upvotes)

print(f"Mean Resolution Time       : {mean_res:.2f} hours")
print(f"Standard Deviation         : {std_res:.2f} hours")
print(f"Variance                   : {variance_res:.2f} hours^2")
print(f"50th Percentile (Median)   : {p50:.2f} hours")
print(f"75th Percentile            : {p75:.2f} hours")
print(f"90th Percentile (P90 SLA)  : {p90:.2f} hours")
print(f"Total Tickets Evaluated    : {total_tickets}")
print(f"SLA Breached Tickets       : {breached_tickets}")
print(f"Overall SLA Compliance     : {compliance_rate:.1f}%")
print(f"Weighted Student Rating    : {weighted_rating:.2f} / 5.0")


# =============================================================================
# PART 3: MATPLOTLIB — Complete 3-Panel Visual Analytics Dashboard
# =============================================================================
print("\n" + "=" * 65)
print("PART 3: MATPLOTLIB (3-Panel Operational Performance Visuals)")
print("=" * 65)

# Create 3-panel figure
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle("FixMyCampus — Facilities Operational Analytics Dashboard", fontsize=15, fontweight="bold", y=1.03)

palette = ["#2B5C43", "#3B82F6", "#F59E0B", "#10B981", "#8B5CF6", "#EC4899", "#6366F1", "#14B8A6"]

# Panel 1: Bar Chart — Average Resolution Hours by Department
axes[0].bar(
    category_summary["Category"], 
    category_summary["Avg_Resolution_Hours"], 
    color=palette[:len(category_summary)],
    edgecolor="#1E293B", 
    linewidth=0.8
)
axes[0].set_title("Avg Resolution Time by Category", fontsize=11, fontweight="bold")
axes[0].set_xlabel("Department", fontsize=10)
axes[0].set_ylabel("Hours", fontsize=10)
axes[0].tick_params(axis="x", rotation=35)
axes[0].grid(axis="y", linestyle="--", alpha=0.5)

# Panel 2: Line + Marker Chart — Target SLA vs. Actual Performance
ticket_labels = [f"#{tid}" for tid in df["Ticket_ID"]]
x_pts = np.arange(len(ticket_labels))

axes[1].plot(x_pts, target_hours, label="Target SLA (Hours)", color="#EF4444", linestyle="--", marker="o", linewidth=2)
axes[1].plot(x_pts, actual_hours, label="Actual Resolution (Hours)", color="#2B5C43", marker="s", linewidth=2)
axes[1].set_xticks(x_pts)
axes[1].set_xticklabels(ticket_labels, rotation=45)
axes[1].set_title("Target SLA vs. Actual Resolution Time", fontsize=11, fontweight="bold")
axes[1].set_xlabel("Ticket ID", fontsize=10)
axes[1].set_ylabel("Hours", fontsize=10)
axes[1].legend(loc="upper left")
axes[1].grid(True, linestyle=":", alpha=0.6)

# Panel 3: Donut Chart — Issue Distribution by Campus Building
bldg_counts = df["Building"].value_counts()
wedges, texts, autotexts = axes[2].pie(
    bldg_counts, 
    labels=bldg_counts.index, 
    autopct="%1.0f%%", 
    startangle=140,
    colors=["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899", "#14B8A6", "#64748B"],
    wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2)  # Donut hole
)
for at in autotexts:
    at.set_fontsize(9)
    at.set_fontweight("bold")
axes[2].set_title("Reported Issues by Campus Location", fontsize=11, fontweight="bold")

plt.tight_layout()

# Save generated chart
output_file = "campus_operations_report.png"
plt.savefig(output_file, dpi=150, bbox_inches="tight")
print(f"Visualization generated and saved to: {output_file}")

# Interactive view (optional when running in terminal/notebook)
# plt.show()
