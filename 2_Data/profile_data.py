"""
Stage 2: first look at the anonymized dataset. Prints a data profile and saves one overview chart.

Run from the project folder:
    python 2_Data/profile_data.py
"""

from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = Path(__file__).resolve().parent
df = pd.read_csv(DATA / "videos_anonymized.csv")
df["publish_date"] = pd.to_datetime(df["publish_date"], format="%b %d, %Y")

has_date = df["publish_date"].notna()
in_scope = has_date & (df["publish_date"] < "2020-01-01")

print(f"Videos in export:                 {len(df)}")
print(f"  with a publish date:            {has_date.sum()}")
print(f"    published Aug 2011-Dec 2019:  {in_scope.sum()}")
print(f"    published after 2019:         {(has_date & ~in_scope).sum()}")
print(f"  no publish date (likely private): {(~has_date).sum()}")
print()
print(f"Lifetime views, all videos:       {df['views'].sum():,.0f}")
print(f"  from in-scope videos:           {df.loc[in_scope, 'views'].sum():,.0f} "
      f"({df.loc[in_scope, 'views'].sum() / df['views'].sum():.1%})")
print()
print("Missing values per column:")
print(df.isna().sum()[df.isna().sum() > 0].to_string())
print()
print(f"avg_pct_viewed over 100%:         {(df['avg_pct_viewed'] > 100).sum()} videos")

# Chart: public videos published per year
per_year = df.loc[in_scope, "publish_date"].dt.year.value_counts().reindex(range(2011, 2020), fill_value=0)

BLUE, TEXT, MUTED, GRID, SURFACE = "#2a78d6", "#0b0b0b", "#52514e", "#e6e5e0", "#fcfcfb"
fig, ax = plt.subplots(figsize=(8, 3.6), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
ax.bar(per_year.index.astype(str), per_year.values, color=BLUE, width=0.6)
for i, v in enumerate(per_year.values):
    ax.text(i, v + 0.6, str(v), ha="center", color=TEXT)
ax.set_title(f"{in_scope.sum()} public videos, 2011–2019: published per year",
             loc="left", fontweight="bold", fontsize=13, color=TEXT)
ax.set_ylabel("Videos", color=MUTED)
ax.set_ylim(0, per_year.max() * 1.18)
ax.tick_params(colors=MUTED)
ax.yaxis.grid(True, color=GRID)
ax.set_axisbelow(True)
for side in ["top", "right"]:
    ax.spines[side].set_visible(False)
for side in ["left", "bottom"]:
    ax.spines[side].set_color(GRID)

(DATA / "images").mkdir(exist_ok=True)
fig.savefig(DATA / "images" / "videos_per_year.png", dpi=150, bbox_inches="tight", facecolor=SURFACE)
print("\nSaved chart to 2_Data/images/videos_per_year.png")
