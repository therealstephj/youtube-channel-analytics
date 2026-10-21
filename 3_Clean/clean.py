"""
Stage 3: clean the anonymized dataset and write an analysis-ready file.

Every rule is logged with how many rows it affected. Nothing is silently deleted: rows that shouldn't be
analyzed are FLAGGED (in_analysis = 0) with a reason, so every total can be traced back to the export.

Inputs:   2_Data/videos_anonymized.csv, 3_Clean/content_categories.csv
Outputs:  3_Clean/videos_clean.csv, 3_Clean/cleaning_log.md

Run from the project folder:
    python 3_Clean/clean.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CLEAN = ROOT / "3_Clean"

df = pd.read_csv(ROOT / "2_Data" / "videos_anonymized.csv")
start_rows, start_views = len(df), df["views"].sum()
log = []


def rule(name, why, rows):
    log.append((name, why, int(rows)))


# ---------------------------------------------------------------- 1. Fix data types
df["publish_date"] = pd.to_datetime(df["publish_date"], format="%b %d, %Y")
rule("Convert `publish_date` text to a real date",
     "Dates stored as text (`Aug 8, 2011`) can't be sorted or grouped by year/weekday", df["publish_date"].notna().sum())

df["avg_view_sec"] = pd.to_timedelta(df["avg_view_duration"]).dt.total_seconds()
rule("Convert `avg_view_duration` from `h:mm:ss` text to seconds (`avg_view_sec`)",
     "You can't average or compare text like `0:01:04`", df["avg_view_sec"].notna().sum())
df = df.drop(columns=["avg_view_duration"])

# ---------------------------------------------------------------- 2. Add content categories
cats = pd.read_csv(CLEAN / "content_categories.csv")
df = df.merge(cats, on="video", how="left")
flags = ["is_reupload", "is_archive_dump", "creator_removed"]
df[flags] = df[flags].fillna(0).astype(int)
rule("Add a content `category` to every public video",
     "The export has no content type. Categories were drafted from the original titles (privately), "
     "then reviewed and corrected by me as the creator", df["category"].notna().sum())

# ---------------------------------------------------------------- 3. Decide what's in the analysis (flag, don't delete)
df["exclude_reason"] = ""


def exclude(mask, reason, why):
    new = mask & (df["exclude_reason"] == "")
    df.loc[new, "exclude_reason"] = reason
    rule(f"Flag as out of scope: {reason}", why, new.sum())


exclude(df["views"].isna(), "no metrics", "One row has no views or other metrics at all, so there's nothing to analyze")
exclude(df["publish_date"].isna(), "unlisted (no publish date)",
        "Mostly unlisted videos: never publicly released, and only ~1% of all views")
exclude(df["publish_date"] >= "2020-01-01", "published after 2019",
        "Outside the Aug 2011 – Dec 2019 period this project studies")
exclude(df["is_reupload"] == 1, "duplicate re-upload",
        "Same video uploaded twice on the same day (a failed/test upload); keeping both would double-count it. "
        "The copy with more views is kept")
exclude(df["creator_removed"] == 1, "outlier (creator's call)",
        "Not representative content: an announcement post and two throwaway uploads, removed after my review")
exclude(df["is_archive_dump"] == 1, "bulk archive upload",
        "11 old clips uploaded on a single day in 2018: an archive dump, not regular releases")
df["in_analysis"] = (df["exclude_reason"] == "").astype(int)

# ---------------------------------------------------------------- 4. Values that look wrong but are real
looped = df["avg_pct_viewed"] > 100
df["is_looped"] = looped.astype(int)
rule("Keep `avg_pct_viewed` over 100%, and flag it as `is_looped`",
     "Not an error: viewers replayed/looped short animations. Capping it at 100% would hide a real behaviour",
     looped.sum())

rule("Leave `ctr_pct` blank when there were no impressions (don't fill with 0)",
     "No impressions means CTR is undefined, not 0%. Filling with 0 would drag averages down",
     df["ctr_pct"].isna().sum())

# ---------------------------------------------------------------- 5. New columns for analysis
df["publish_year"] = df["publish_date"].dt.year.astype("Int64")
df["publish_weekday"] = df["publish_date"].dt.day_name()
df["duration_min"] = (df["duration_sec"] / 60).round(2)
df["length_bucket"] = pd.cut(df["duration_sec"], bins=[0, 30, 60, 120, 300, np.inf],
                             labels=["<30s", "30s–1m", "1–2m", "2–5m", "5m+"], right=False)

per_1k = df["views"].replace(0, np.nan) / 1000
for col in ["subs_gained", "likes", "comments", "shares"]:
    df[f"{col}_per_1k_views"] = (df[col] / per_1k).round(2)

df["views_after_2019"] = df["views"] - df["views_2011_2019"]
df["long_tail_pct"] = (df["views_after_2019"] / df["views"].replace(0, np.nan) * 100).round(1)
rule("Add helper columns: year, weekday, length bucket, per-1,000-view rates, views after 2019, long-tail %",
     "Rates make big and small videos comparable; long-tail % answers question 6", len(df))

# ---------------------------------------------------------------- 6. Validation checks (stop if any fail)
a = df[df["in_analysis"] == 1]
checks = {
    "Row count unchanged (nothing deleted)": len(df) == start_rows,
    "Total views unchanged": np.isclose(df["views"].sum(), start_views),
    "Video IDs are unique": df["video"].is_unique,
    "Every analysis video has a publish date in Aug 2011 – Dec 2019":
        a["publish_date"].between("2011-08-01", "2019-12-31").all(),
    "Every analysis video has a category": a["category"].notna().all(),
    "Every analysis video has 2011–2019 views (for the long-tail check)": a["views_2011_2019"].notna().all(),
    "No negative 'views after 2019'": (a["views_after_2019"] >= 0).all(),
}
for name, ok in checks.items():
    print(("PASS  " if ok else "FAIL  ") + name)
assert all(checks.values()), "Validation failed: see above"

# ---------------------------------------------------------------- Save
cols = ["video", "in_analysis", "exclude_reason", "category", "publish_date", "publish_year", "publish_weekday",
        "duration_sec", "duration_min", "length_bucket", "views", "watch_hours", "avg_view_sec", "avg_pct_viewed",
        "is_looped", "subs_gained", "subs_net", "likes", "comments", "shares", "subs_gained_per_1k_views",
        "likes_per_1k_views", "comments_per_1k_views", "shares_per_1k_views", "impressions", "ctr_pct",
        "views_2011_2019", "views_after_2019", "long_tail_pct", "watch_hours_2011_2019", "subs_gained_2011_2019",
        "title_length", "is_reupload", "is_archive_dump", "creator_removed"]
df[cols].to_csv(CLEAN / "videos_clean.csv", index=False)

summary = df.groupby(df["exclude_reason"].replace("", "✅ in analysis"))["views"].agg(["size", "sum"])
lines = ["# Cleaning Log", "",
         "_Generated by [`clean.py`](clean.py). Re-run it and this file is rebuilt._", "",
         "| # | Rule | Why | Rows affected |", "|---|---|---|---|"]
lines += [f"| {i} | {n} | {w} | {r:,} |" for i, (n, w, r) in enumerate(log, 1)]
lines += ["", "## Where every video ended up", "", "| Status | Videos | Lifetime views |", "|---|---|---|"]
lines += [f"| {k} | {int(r['size'])} | {r['sum']:,.0f} |" for k, r in summary.sort_values("size", ascending=False).iterrows()]
lines += [f"| **Total** | **{len(df)}** | **{df['views'].sum():,.0f}** |", "", "## Validation checks", ""]
lines += [f"- {'✅' if ok else '❌'} {name}" for name, ok in checks.items()]
(CLEAN / "cleaning_log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"\n{len(a)} videos in analysis ({a['views'].sum():,.0f} views). Saved videos_clean.csv + cleaning_log.md")
