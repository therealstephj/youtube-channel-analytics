"""
Stage 2: turn the raw YouTube Studio exports into one anonymized, GitHub-safe dataset.

Inputs (kept on my computer only, see .gitignore):
    2_Data/raw/lifetime/Table data.csv     one row per video, lifetime totals
    2_Data/raw/2011-2019/Table data.csv    same videos, Aug 2011 - Dec 2019 only

Output:
    2_Data/videos_anonymized.csv           one row per video, no titles or video IDs

Nothing is cleaned or removed here; that's Stage 3. This step only combines, renames and anonymizes.

Run from the project folder:
    python 2_Data/build_dataset.py
"""

from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent
RAW = DATA / "raw"

RENAME = {
    "Content": "video_id",
    "Video title": "title",
    "Video publish time": "publish_date",
    "Duration": "duration_sec",
    "Average view duration": "avg_view_duration",
    "Average percentage viewed (%)": "avg_pct_viewed",
    "Subscribers gained": "subs_gained",
    "Likes": "likes",
    "Comments added": "comments",
    "Shares": "shares",
    "Views": "views",
    "Watch time (hours)": "watch_hours",
    "Subscribers": "subs_net",
    "Thumbnail impressions": "impressions",
    "Thumbnail click-through rate (%)": "ctr_pct",
}


def load(folder):
    df = pd.read_csv(RAW / folder / "Table data.csv").rename(columns=RENAME)
    return df[df["video_id"] != "Total"]  # first row is a channel-wide total, not a video


lifetime = load("lifetime")
active = load("2011-2019")

# Views earned during the active years, so Stage 4 can measure the "long tail" after 2019
df = lifetime.merge(
    active[["video_id", "views", "watch_hours", "subs_gained"]].rename(columns={
        "views": "views_2011_2019",
        "watch_hours": "watch_hours_2011_2019",
        "subs_gained": "subs_gained_2011_2019",
    }),
    on="video_id", how="left",
)

# Anonymize: number videos by publish date (oldest = 1), then drop titles and YouTube IDs
df["_sort_date"] = pd.to_datetime(df["publish_date"], format="%b %d, %Y", errors="coerce")
df = df.sort_values(["_sort_date", "duration_sec"], na_position="last").reset_index(drop=True)
df.insert(0, "video", [f"V{i:03d}" for i in range(1, len(df) + 1)])
df["title_length"] = df["title"].str.len()  # keep a harmless feature from the title

# Private lookup (V001 -> real title), so categories can be assigned by hand. Stays in raw/, off GitHub.
df[["video", "video_id", "title", "publish_date", "duration_sec", "views"]].to_csv(RAW / "video_key_PRIVATE.csv", index=False)
df = df.drop(columns=["video_id", "title", "_sort_date"])

df.to_csv(DATA / "videos_anonymized.csv", index=False)
print(f"Saved {len(df)} videos to {DATA / 'videos_anonymized.csv'}")
