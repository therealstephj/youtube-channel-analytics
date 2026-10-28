"""
Stage 6: the two summary visuals for the final report.
    6_Report/kpi_summary.png   headline KPIs, computed from the clean data
    6_Report/scorecard.png     my Stage 1 predictions vs what the data showed

Run from the project folder:
    python 6_Report/make_report_visuals.py
"""

from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "6_Report"
df = pd.read_csv(ROOT / "3_Clean" / "videos_clean.csv")
a = df[df["in_analysis"] == 1]

BLUE, TEXT, MUTED, GRID, SURFACE, CARD = "#2a78d6", "#0b0b0b", "#52514e", "#e6e5e0", "#fcfcfb", "#f3f2ee"
GOOD, WARN, BAD = "#008300", "#c98500", "#e34948"

# ---------------------------------------------------------------- KPIs (all computed, nothing typed in)
music = a[a["category"] == "Music animation"]
top7 = a.nlargest(7, "views")
kpis = [
    (f"{a['views'].sum():,.0f}", "lifetime views", f"across {len(a)} public videos, 2011–2019"),
    (f"{a['watch_hours'].sum():,.0f}", "hours watched", f"{a['subs_gained'].sum():,.0f} subscribers gained"),
    (f"{music['views'].sum() / a['views'].sum():.0%}", "of views from music animations",
     f"which were only {len(music) / len(a):.0%} of videos made"),
    (f"{top7['views'].sum() / a['views'].sum():.0%}", "of views from the top 7 videos",
     f"and {top7['subs_gained'].sum() / a['subs_gained'].sum():.0%} of subscribers"),
    (f"{a.loc[a['length_bucket'] == '<30s', 'avg_pct_viewed'].median():.0f}%", "watched on videos under 30s",
     f"vs {a.loc[a['length_bucket'] == '5m+', 'avg_pct_viewed'].median():.0f}% on videos over 5 min"),
    (f"{(a['views_after_2019'] > 0).sum()} / {len(a)}", "videos still watched since 2020",
     f"{a['views_after_2019'].sum():,.0f} views after I stopped posting"),
]

fig = plt.figure(figsize=(11, 5.4), facecolor=SURFACE)
fig.text(0.02, 0.95, "What made my videos work: the numbers", fontsize=17, fontweight="bold", color=TEXT, va="top")
fig.text(0.02, 0.875, "8 years of my own YouTube Studio data · 66 public sprite & game animation videos, Aug 2011 – Dec 2019",
         fontsize=10.5, color=MUTED, va="top")
for i, (big, label, sub) in enumerate(kpis):
    col, row = i % 3, i // 3
    x, y, w, h = 0.02 + col * 0.33, 0.43 - row * 0.40, 0.31, 0.35
    ax = fig.add_axes([x, y, w, h])
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.06",
                                transform=ax.transAxes, facecolor=CARD, edgecolor=GRID, linewidth=1))
    ax.text(0.07, 0.68, big, fontsize=27, fontweight="bold", color=BLUE if i in (2, 3) else TEXT,
            transform=ax.transAxes, va="center")
    ax.text(0.07, 0.36, label, fontsize=11, color=TEXT, transform=ax.transAxes, va="center")
    ax.text(0.07, 0.17, sub, fontsize=9.2, color=MUTED, transform=ax.transAxes, va="center")
fig.savefig(OUT / "kpi_summary.png", dpi=170, bbox_inches="tight", facecolor=SURFACE)
plt.close(fig)
print("Saved kpi_summary.png")

# ---------------------------------------------------------------- Scorecard
rows = [
    ("My later videos did better", "✗  WRONG", BAD, "2012–2013 was my peak: 71% of views"),
    ("Short = holds attention,\nlong = more watch time", "½  HALF RIGHT", WARN, "Short won on retention AND watch time"),
    ("Posting day doesn't matter", "✓  RIGHT", GOOD, "No significant difference between days"),
    ("A few videos did most of the work", "✓  RIGHT", GOOD, "Top 7 videos: 54% of views, 64% of subs"),
    ("Old videos still get views", "✓  RIGHT", GOOD, "61 of 66 still watched since 2020"),
]
fig, ax = plt.subplots(figsize=(10, 4.8), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
ax.axis("off")
ax.text(0, 1.0, "I predicted what made my videos work. Then I checked the data.", fontsize=15,
        fontweight="bold", color=TEXT, transform=ax.transAxes, va="top")
ax.text(0, 0.91, "5 predictions written down before looking at any data  ·  Score: 3 right, 1 half right, 1 wrong",
        fontsize=10, color=MUTED, transform=ax.transAxes, va="top")
for i, (pred, verdict, color, evidence) in enumerate(rows):
    y = 0.75 - i * 0.16
    ax.plot([0, 1], [y + 0.075, y + 0.075], color=GRID, lw=1, transform=ax.transAxes)
    ax.text(0, y, pred, fontsize=10.5, color=TEXT, transform=ax.transAxes, va="center")
    ax.text(0.38, y, verdict, fontsize=10.5, fontweight="bold", color=color, transform=ax.transAxes, va="center")
    ax.text(0.58, y, evidence, fontsize=10, color=MUTED, transform=ax.transAxes, va="center")
fig.savefig(OUT / "scorecard.png", dpi=170, bbox_inches="tight", facecolor=SURFACE)
plt.close(fig)
print("Saved scorecard.png")
