"""Stage 3 chart: how 337 exported videos became the analysis set. Run: python 3_Clean/cleaning_funnel.py"""

from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

CLEAN = Path(__file__).resolve().parent
df = pd.read_csv(CLEAN / "videos_clean.csv")

steps = [("Exported from YouTube Studio", len(df))]
remaining = len(df)
for label, reasons in [
    ("Remove unlisted / empty", ["unlisted (no publish date)", "no metrics"]),
    ("Remove posted after 2019", ["published after 2019"]),
    ("Remove bulk archive upload", ["bulk archive upload"]),
    ("Remove duplicate re-uploads", ["duplicate re-upload"]),
]:
    remaining -= df["exclude_reason"].isin(reasons).sum()
    steps.append((label, remaining))
share = df.loc[df["in_analysis"] == 1, "views"].sum() / df["views"].sum()

BLUE, GRAY, TEXT, MUTED, SURFACE = "#2a78d6", "#b9b8b2", "#0b0b0b", "#52514e", "#fcfcfb"
fig, ax = plt.subplots(figsize=(9, 3.8), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
labels = [s[0] for s in steps][::-1]
values = [s[1] for s in steps][::-1]
colors = [BLUE] + [GRAY] * (len(steps) - 1)
ax.barh(labels, values, color=colors, height=0.6)
for i, v in enumerate(values):
    ax.text(v + 4, i, f"{v}", va="center", color=TEXT, fontweight="bold" if i == 0 else "normal")
ax.text(values[0] + 30, 0, f"← {values[0]} videos analyzed, holding {share:.0%} of all views",
        va="center", color=TEXT, fontsize=10)
ax.set_title("From 337 exported videos to a clean analysis set", loc="left", fontweight="bold", fontsize=13)
ax.set_xlim(0, max(values) * 1.12)
ax.set_xticks([])
for side in ["top", "right", "bottom"]:
    ax.spines[side].set_visible(False)
ax.spines["left"].set_color("#e6e5e0")
ax.tick_params(colors=MUTED, length=0)

(CLEAN / "images").mkdir(exist_ok=True)
fig.savefig(CLEAN / "images" / "cleaning_funnel.png", dpi=150, bbox_inches="tight", facecolor=SURFACE)
print("Saved 3_Clean/images/cleaning_funnel.png")
