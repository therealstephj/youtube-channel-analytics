# Stage 4: Analyze

👉 **[Full analysis notebook](analysis.ipynb)** (code, numbers, quick charts and plain-English answers) ·
**[SQL version](queries.sql)** (every question cross-checked in SQL)

66 public videos, Aug 2011 – Dec 2019. Comparisons mostly use **medians** because a few viral videos would
distort averages. Two answers are backed by significance tests (Kruskal-Wallis).

## Answers to the six questions

| # | Question | Answer |
|---|---|---|
| 01 | **Growth:** how did results change over the years? | The channel peaked in **2012–2013**: those years produced **~71% of all views**, with the best typical video (2013 median ≈ 6,500 views) |
| 02 | **Length:** did longer videos lose people? | **Yes, strongly** (correlation −0.90). Under 30s: viewers watched **109%** (looping). Over 5 min: **23%**. The **30s–2m** range was the sweet spot for views *and* watch time |
| 03 | **Timing:** did the posting day matter? | **No reliable difference.** Only 6–14 videos per day, and the test isn't significant (p = 0.055) |
| 04 | **Engagement:** what turned viewers into subscribers? | **7 videos (10%) earned 54% of views and 64% of subscribers.** Animations converted best (~2.3–2.5 subs per 1,000 views vs ~1.5–1.7 for gameplay and skits) |
| 05 | **Content:** which types performed best? | **Music animations: 29% of videos, 61% of views, 69% of subscribers.** Gameplay: 27% of videos, only 7% of views. Comedy animation had the highest *typical* views, so it was more consistent, less hit-driven (p < 0.001) |
| 06 | **Long tail:** are videos still watched? | **Yes, slowly.** ~37,800 views since 2020 (7% of lifetime), and **61 of 66** videos still get views. Comedy animations aged best (11.5%) |

## Prediction scorecard

| # | My prediction (Stage 1) | Verdict |
|---|---|---|
| 1 | Later videos performed better | ❌ Wrong: 2012–2013 was the peak |
| 2 | Short = higher retention, long = more watch time | ½ Retention right, watch time wrong |
| 3 | Posting day made little difference | ✅ Right |
| 4 | A few videos brought most views and subscribers | ✅ Right |
| 5 | Old videos still get views | ✅ Right |

## Limitations
- **66 videos is a small sample.** Patterns are clear, but day-of-week and smaller categories are thin.
- **Correlation, not causation.** For example, short videos did better, but my short videos were also mostly animations.
- **Categories were assigned by me**, from memory and titles.
- **YouTube's algorithm changed a lot** between 2011 and 2019, so some year-to-year differences are the platform, not the content.
