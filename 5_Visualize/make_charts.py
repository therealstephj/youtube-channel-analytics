"""
Stage 5: one presentation-ready chart per question. Each title states the finding, not just the topic.

Input:  3_Clean/videos_clean.csv (in_analysis = 1)
Output: 5_Visualize/charts/*.png

Run from the project folder:
    python 5_Visualize/make_charts.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "5_Visualize" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(ROOT / "3_Clean" / "videos_clean.csv")
a = df[df["in_analysis"] == 1].copy()

# One palette for every chart: blue = the point of the chart, gray = context
BLUE, GRAY, TEXT, MUTED, GRID, SURFACE = "#2a78d6", "#b9b8b2", "#0b0b0b", "#52514e", "#e6e5e0", "#fcfcfb"
plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
    "text.color": TEXT, "font.size": 10.5, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
})


def finish(fig, ax, name, title, subtitle, note=None):
    fig.text(0.01, 1.0, title, fontsize=14, fontweight="bold", color=TEXT, ha="left", va="bottom")
    fig.text(0.01, 0.985, subtitle, fontsize=10, color=MUTED, ha="left", va="top")
    if note:
        fig.text(0.01, -0.02, note, fontsize=8.5, color=MUTED, ha="left", va="top")
    fig.subplots_adjust(top=0.86)
    fig.savefig(OUT / f"{name}.png", dpi=170, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {name}.png")


SOURCE = "Source: my YouTube Studio export · 66 public videos, Aug 2011 – Dec 2019"

# ---------------------------------------------------------------- 1. Content: made vs watched
cat = a.groupby("category").agg(videos=("video", "size"), views=("views", "sum"), subs=("subs_gained", "sum"))
cat["pct_videos"] = cat["videos"] / cat["videos"].sum() * 100
cat["pct_views"] = cat["views"] / cat["views"].sum() * 100
cat = cat.sort_values("pct_views")

fig, ax = plt.subplots(figsize=(9, 4.2))
y = np.arange(len(cat))
ax.barh(y + 0.19, cat["pct_videos"], height=0.36, color=GRAY, label="% of videos I made")
ax.barh(y - 0.19, cat["pct_views"], height=0.36, color=BLUE, label="% of views they earned")
for i, (pv, pw) in enumerate(zip(cat["pct_videos"], cat["pct_views"])):
    ax.text(pv + 0.8, i + 0.19, f"{pv:.0f}%", va="center", color=MUTED, fontsize=9.5)
    ax.text(pw + 0.8, i - 0.19, f"{pw:.0f}%", va="center", color=TEXT, fontsize=9.5, fontweight="bold")
ax.set_yticks(y, cat.index)
ax.set_xlim(0, 70)
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
ax.set_xlabel("% of total")
ax.legend(frameon=False, loc="lower right")
finish(fig, ax, "01_content_made_vs_watched",
       "Music animations: 29% of what I made, 61% of what people watched",
       "Share of videos made vs share of lifetime views, by content type", SOURCE)

# ---------------------------------------------------------------- 2. Length vs retention
ORDER = ["<30s", "30s–1m", "1–2m", "2–5m", "5m+"]
ln = a.groupby("length_bucket").agg(pct=("avg_pct_viewed", "median"), n=("video", "size")).reindex(ORDER)
rho = stats.spearmanr(a["duration_sec"], a["avg_pct_viewed"])[0]

fig, ax = plt.subplots(figsize=(9, 4.2))
ax.bar(ORDER, ln["pct"], color=BLUE, width=0.6)
ax.axhline(100, color=MUTED, linestyle="--", linewidth=1)
ax.text(4.45, 101.5, "100% = watched once, start to finish", ha="right", va="bottom", color=MUTED, fontsize=9)
for i, (v, n) in enumerate(zip(ln["pct"], ln["n"])):
    if 88 < v < 100:  # would collide with the 100% line, so label inside the bar
        ax.text(i, v - 7, f"{v:.0f}%", ha="center", fontweight="bold", color="white")
    else:
        ax.text(i, v + 3, f"{v:.0f}%", ha="center", fontweight="bold")
    ax.text(i, 4, f"{n} videos", ha="center", color="white", fontsize=8.5)
ax.set_ylim(0, 128)
ax.set_xlabel("Video length")
ax.set_ylabel("Typical % of the video watched")
ax.grid(axis="x", visible=False)
finish(fig, ax, "02_length_vs_retention",
       "The shorter the video, the more of it people watched",
       f"Median % of each video watched, by length · correlation {rho:.2f} (very strong)",
       "Over 100% means viewers replayed it. 80% of videos under 30s were looped.  ·  " + SOURCE)

# ---------------------------------------------------------------- 3. Concentration (Pareto)
ranked = a.sort_values("views", ascending=False)
cum_views = ranked["views"].cumsum() / ranked["views"].sum() * 100
cum_subs = ranked["subs_gained"].cumsum() / ranked["subs_gained"].sum() * 100
x = np.arange(1, len(ranked) + 1)
top_n = 7

fig, ax = plt.subplots(figsize=(9, 4.2))
ax.plot(x, cum_views.values, color=BLUE, linewidth=2.2, label="% of all views")
ax.plot(x, cum_subs.values, color=GRAY, linewidth=2.2, label="% of all subscribers gained")
ax.axvspan(0.5, top_n + 0.5, color=BLUE, alpha=0.07, linewidth=0)
ax.scatter([top_n], [cum_views.iloc[top_n - 1]], color=BLUE, s=55, zorder=3, edgecolor=SURFACE, linewidth=2)
ax.scatter([top_n], [cum_subs.iloc[top_n - 1]], color=GRAY, s=55, zorder=3, edgecolor=SURFACE, linewidth=2)
ax.annotate(f"Top {top_n} videos:\n{cum_views.iloc[top_n - 1]:.0f}% of views\n{cum_subs.iloc[top_n - 1]:.0f}% of subscribers",
            xy=(top_n, cum_views.iloc[top_n - 1]), xytext=(15, 30), textcoords="data", fontsize=10,
            fontweight="bold", color=TEXT, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
ax.set_xlim(0.5, len(ranked) + 0.5)
ax.set_ylim(0, 105)
ax.set_xlabel("Videos, ranked from most to least viewed")
ax.set_ylabel("Cumulative %")
ax.legend(frameon=False, loc="lower right")
finish(fig, ax, "03_few_hits_did_most_work",
       "A handful of hits did most of the work",
       "Running total of views and subscribers as each video is added, biggest first", SOURCE)

# ---------------------------------------------------------------- 4. Growth by year
yr = a.groupby("publish_year").agg(views=("views", "sum"), n=("video", "size"))
yr.index = yr.index.astype(int)
yr = yr.reindex(range(2011, 2020), fill_value=0)
yr["pct"] = yr["views"] / yr["views"].sum() * 100

fig, ax = plt.subplots(figsize=(9, 4.2))
colors = [BLUE if y_ in (2012, 2013) else GRAY for y_ in yr.index]
ax.bar(range(len(yr)), yr["pct"], color=colors, width=0.6)
for i, (p, n) in enumerate(zip(yr["pct"], yr["n"])):
    if n:
        ax.text(i, p + 1, f"{p:.0f}%", ha="center", fontweight="bold" if colors[i] == BLUE else "normal")
ax.set_xticks(range(len(yr)), [f"{y_}\n{n} videos" for y_, n in zip(yr.index, yr["n"])], fontsize=9)
ax.set_ylim(0, 45)
ax.tick_params(axis="x", length=0)
ax.set_ylabel("% of all views")
ax.grid(axis="x", visible=False)
finish(fig, ax, "04_peak_was_2012_2013",
       "My peak was 2012–2013: 71% of all views",
       "Share of lifetime views, by the year the video was published",
       "2017–2018: no regular uploads (2018 was a bulk upload of old clips, excluded).  ·  " + SOURCE)

# ---------------------------------------------------------------- 5. Weekday (noise)
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
p_day = stats.kruskal(*[g["views"] for _, g in a.groupby("publish_weekday")])[1]
rng = np.random.default_rng(7)

fig, ax = plt.subplots(figsize=(9, 4.2))
for i, d in enumerate(DAYS):
    v = a.loc[a["publish_weekday"] == d, "views"]
    ax.scatter(i + rng.uniform(-0.15, 0.15, len(v)), v, s=28, color=GRAY, alpha=0.9, edgecolor=SURFACE, linewidth=0.8)
    ax.plot([i - 0.28, i + 0.28], [v.median()] * 2, color=BLUE, linewidth=2.5)
ax.set_yscale("log")
ax.set_xticks(range(7), [d[:3] for d in DAYS])
ax.set_yticks([100, 1_000, 10_000, 100_000], ["100", "1K", "10K", "100K"])
ax.set_ylabel("Views per video (log scale)")
ax.grid(axis="x", visible=False)
ax.plot([], [], color=BLUE, linewidth=2.5, label="Median")
ax.scatter([], [], color=GRAY, s=28, label="One video")
ax.legend(frameon=False, loc="upper right", ncol=2)
finish(fig, ax, "05_posting_day_didnt_matter",
       "The posting day didn't matter",
       f"Views per video by weekday: the spread within each day dwarfs the gaps between days (p = {p_day:.3f}, not significant)",
       SOURCE)

# ---------------------------------------------------------------- 6. Long tail
tail = a.groupby("category").agg(after=("views_after_2019", "sum"), total=("views", "sum"),
                                  still=("views_after_2019", lambda s: (s > 0).sum()), n=("video", "size"))
tail["pct"] = tail["after"] / tail["total"] * 100
tail = tail.sort_values("pct")
overall = a["views_after_2019"].sum() / a["views"].sum() * 100

fig, ax = plt.subplots(figsize=(9, 3.8))
ax.barh(tail.index, tail["pct"], color=[BLUE if c == tail["pct"].idxmax() else GRAY for c in tail.index], height=0.55)
for i, p in enumerate(tail["pct"]):
    ax.text(p + 0.25, i, f"{p:.1f}%", va="center", fontsize=10, fontweight="bold" if i == len(tail) - 1 else "normal")
ax.set_yticks(range(len(tail)), [f"{c}\n{s} of {n} still watched" for c, s, n in zip(tail.index, tail["still"], tail["n"])])
ax.axvline(overall, color=MUTED, linestyle="--", linewidth=1)
ax.text(overall + 0.15, len(tail) - 0.45, f"all videos: {overall:.1f}%", color=MUTED, fontsize=9)
ax.set_xlim(0, 14)
ax.set_xlabel("% of each category's lifetime views earned since Jan 2020")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
finish(fig, ax, "06_still_watched_years_later",
       f"Years after I stopped, {(a['views_after_2019'] > 0).sum()} of {len(a)} videos still get views",
       f"{a['views_after_2019'].sum():,.0f} views since 2020. Comedy animations aged best", SOURCE)
