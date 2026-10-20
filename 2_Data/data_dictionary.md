# Data Dictionary: `videos_anonymized.csv`

One row per video. **337 rows**, built from two YouTube Studio exports (Analytics → Advanced mode → Content):
a **lifetime** export and an **Aug 2011 – Dec 2019** export, joined on video.

Unless a column name says otherwise, numbers are **lifetime** totals (up to Oct 2026).

| Column | Type | Meaning | Notes |
|---|---|---|---|
| `video` | text | Anonymous ID: `V001` = oldest video | Replaces the YouTube video ID and title for privacy |
| `publish_date` | date (text) | Day the video went public, e.g. `Aug 8, 2011` | **Blank for 248 videos**, which are mostly unlisted videos |
| `duration_sec` | number | Video length in seconds | |
| `avg_view_duration` | text `h:mm:ss` | How long a typical view lasted | Stored as text; convert to seconds in Stage 3 |
| `avg_pct_viewed` | % | Average share of the video watched per view | **Can be over 100%** when viewers replay or loop a video, common for short animations |
| `views` | number | Total views | |
| `watch_hours` | number | Total hours watched across all views | |
| `subs_gained` | number | Subscribers gained from this video | |
| `subs_net` | number | Subscribers gained minus lost | |
| `likes` | number | Likes | |
| `comments` | number | Comments added | |
| `shares` | number | Times shared | |
| `impressions` | number | Times the thumbnail was shown on YouTube | Only counted since YouTube started tracking impressions, so it misses early-life impressions for old videos |
| `ctr_pct` | % | Click-through rate: % of impressions that became a view | Blank when there were no impressions |
| `views_2011_2019` | number | Views earned **Aug 2011 – Dec 2019** only | Blank for videos published after 2019 or without data in that window |
| `watch_hours_2011_2019` | number | Watch hours, Aug 2011 – Dec 2019 only | Same as above |
| `subs_gained_2011_2019` | number | Subscribers gained, Aug 2011 – Dec 2019 only | Same as above |
| `title_length` | number | Number of characters in the original title | The only thing kept from the title |

## What was removed for privacy
- **Video titles** and **YouTube video IDs**. Either one would identify the channel.
- **Daily chart data** (`Chart data.csv`), which repeats titles and only covers the top 5 videos.

The raw exports stay on my computer and are excluded from GitHub (see `.gitignore`).

## Control totals
A quick check that nothing was lost while combining the files:

| Check | Value |
|---|---|
| Videos in lifetime export | 337 |
| Videos in 2011–2019 export | 288 (all 288 matched a lifetime row) |
| Lifetime views, sum of video rows | 542,456 |
| Lifetime views, YouTube's own "Total" row | 543,777 |

The ~1,300-view gap (0.2%) is most likely views on **deleted** videos, which YouTube still counts in the
channel total but no longer lists as rows.
