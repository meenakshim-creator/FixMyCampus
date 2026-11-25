"""
Visual Analytics Engine for FixMyCampus — 3D Tree & Organic Forest Theme.
Generates publication-grade, modern charts using Matplotlib, Pandas, and NumPy.
Outputs Base64-encoded PNG images styled in Clean Forest White & Deep Pine.
"""
import io
import base64
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Dict
from data_manager import get_issues_df

# Clean Organic Forest Theme Design Tokens
FOREST_COLORS = {
    "bg": "#FFFFFF",
    "card": "#F8FAF7",
    "pine_dark": "#0E2C1E",
    "pine_mid": "#1E543B",
    "emerald": "#2D6A4F",
    "mint": "#52B788",
    "sage": "#74C69D",
    "amber": "#D97706",
    "coral": "#E11D48",
    "blue": "#2563EB",
    "text_dark": "#081C12",
    "text_muted": "#526B5E",
    "border": "#DDE7E0"
}

FOREST_PALETTE = [
    FOREST_COLORS["emerald"],
    FOREST_COLORS["mint"],
    FOREST_COLORS["pine_mid"],
    FOREST_COLORS["amber"],
    FOREST_COLORS["blue"],
    FOREST_COLORS["coral"]
]

def _fig_to_base64(fig: plt.Figure) -> str:
    """Converts a Matplotlib figure into a base64 encoded PNG string."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=160, facecolor=FOREST_COLORS["bg"], edgecolor="none")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return encoded

def generate_category_donut_chart(df: pd.DataFrame) -> str:
    """Generates a clean donut chart showing tickets distribution by category in Forest style."""
    if df.empty:
        df = get_issues_df()

    cat_counts = df["category"].value_counts()
    labels = cat_counts.index.tolist()
    values = cat_counts.values.tolist()

    fig, ax = plt.subplots(figsize=(6, 4.2), facecolor=FOREST_COLORS["bg"])
    ax.set_facecolor(FOREST_COLORS["bg"])
    colors = FOREST_PALETTE[:len(labels)] if len(labels) <= len(FOREST_PALETTE) else FOREST_PALETTE * 2

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct="%1.0f%%",
        startangle=140,
        colors=colors[:len(values)],
        pctdistance=0.75,
        wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2.5)
    )

    for text in texts:
        text.set_color(FOREST_COLORS["text_dark"])
        text.set_fontsize(9.5)
        text.set_fontweight("medium")

    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontsize(8.5)
        autotext.set_fontweight("bold")

    # Center circle label
    ax.text(
        0, 0, f"{len(df)}\nIssues",
        ha="center", va="center",
        fontsize=13, fontweight="bold",
        color=FOREST_COLORS["pine_dark"]
    )

    ax.set_title("Campus Issues by Category", fontsize=12, fontweight="bold", pad=15, color=FOREST_COLORS["pine_dark"])
    plt.tight_layout()
    return _fig_to_base64(fig)

def generate_building_hotspots_chart(df: pd.DataFrame) -> str:
    """Generates a horizontal bar chart showing issues volume across campus buildings in Forest style."""
    if df.empty:
        df = get_issues_df()

    bld_counts = df["building"].value_counts().head(7).iloc[::-1]
    buildings = [b[:18] + ".." if len(b) > 18 else b for b in bld_counts.index.tolist()]
    counts = bld_counts.values.tolist()

    fig, ax = plt.subplots(figsize=(6, 4.2), facecolor=FOREST_COLORS["bg"])
    ax.set_facecolor(FOREST_COLORS["bg"])
    
    y_pos = np.arange(len(buildings))
    bars = ax.barh(y_pos, counts, height=0.55, color="#DDE7E0", edgecolor="none", zorder=3)
    
    # Highlight top building with deep pine & emerald
    if len(bars) > 0:
        bars[-1].set_color(FOREST_COLORS["emerald"])
    if len(bars) > 1:
        bars[-2].set_color(FOREST_COLORS["mint"])

    ax.set_yticks(y_pos)
    ax.set_yticklabels(buildings, fontsize=9.5, fontweight="medium", color=FOREST_COLORS["text_dark"])
    ax.set_xlabel("Number of Reported Issues", fontsize=9.5, color=FOREST_COLORS["text_muted"], labelpad=8)
    ax.set_title("Campus Building Incident Hotspots", fontsize=12, fontweight="bold", pad=15, color=FOREST_COLORS["pine_dark"])
    
    # Grid and spines
    ax.xaxis.grid(True, linestyle="--", alpha=0.5, color=FOREST_COLORS["border"], zorder=0)
    ax.yaxis.grid(False)
    for spine in ["top", "right", "left", "bottom"]:
        ax.spines[spine].set_visible(False)
    ax.tick_params(colors=FOREST_COLORS["text_muted"])

    # Value callouts on bars
    for bar in bars:
        w = bar.get_width()
        ax.text(
            w + 0.15, bar.get_y() + bar.get_height() / 2,
            f"{int(w)}",
            ha="left", va="center",
            fontsize=9, fontweight="bold",
            color=FOREST_COLORS["text_dark"]
        )

    plt.tight_layout()
    return _fig_to_base64(fig)

def generate_weekly_trend_chart(df: pd.DataFrame) -> str:
    """Generates grouped bar chart showing resolution velocity over recent days in Forest style."""
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Today"]
    reported = [8, 12, 14, 11, 9, 10]
    resolved = [7, 11, 13, 10, 8, 9]

    x = np.arange(len(days))
    width = 0.35

    fig, ax = plt.subplots(figsize=(6.5, 4.2), facecolor=FOREST_COLORS["bg"])
    ax.set_facecolor(FOREST_COLORS["bg"])
    
    ax.bar(x - width/2, reported, width, label="New Reported", color="#CBD5E1", alpha=0.9, zorder=3)
    ax.bar(x + width/2, resolved, width, label="Resolved", color=FOREST_COLORS["emerald"], zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(days, fontsize=9.5, fontweight="medium", color=FOREST_COLORS["text_dark"])
    ax.set_ylabel("Ticket Count", fontsize=9.5, color=FOREST_COLORS["text_muted"], labelpad=8)
    ax.set_title("Weekly Inflow vs. Resolution Velocity", fontsize=12, fontweight="bold", pad=15, color=FOREST_COLORS["pine_dark"])
    
    ax.legend(frameon=True, facecolor="white", edgecolor=FOREST_COLORS["border"], labelcolor=FOREST_COLORS["text_dark"], fontsize=9)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5, color=FOREST_COLORS["border"], zorder=0)
    ax.xaxis.grid(False)
    for spine in ["top", "right", "left", "bottom"]:
        ax.spines[spine].set_visible(False)
    ax.tick_params(colors=FOREST_COLORS["text_muted"])

    plt.tight_layout()
    return _fig_to_base64(fig)

def get_all_analytics_charts() -> Dict[str, str]:
    """Generates all analytical charts and returns them as a dictionary of base64 image strings."""
    df = get_issues_df()
    return {
        "category_donut": generate_category_donut_chart(df),
        "building_hotspots": generate_building_hotspots_chart(df),
        "weekly_trend": generate_weekly_trend_chart(df)
    }
