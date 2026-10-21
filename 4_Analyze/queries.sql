-- Stage 4: the six questions in SQL.
-- Runs against table `videos` = 3_Clean/videos_clean.csv filtered to in_analysis = 1
-- (the notebook loads it into SQLite and runs every query below).

-- name: q1_growth_by_year
-- How did output and results change year by year?
SELECT
    publish_year,
    COUNT(*)                                             AS videos,
    SUM(views)                                           AS total_views,
    ROUND(100.0 * SUM(views) / (SELECT SUM(views) FROM videos), 1) AS pct_of_all_views,
    SUM(subs_gained)                                     AS subs_gained
FROM videos
GROUP BY publish_year
ORDER BY publish_year;

-- name: q2_length_vs_retention
-- Did longer videos keep people watching, or lose them?
SELECT
    length_bucket,
    COUNT(*)                          AS videos,
    ROUND(AVG(avg_pct_viewed), 1)     AS avg_pct_viewed,
    ROUND(AVG(avg_view_sec), 0)       AS avg_seconds_watched,
    ROUND(SUM(watch_hours), 0)        AS total_watch_hours,
    SUM(is_looped)                    AS videos_looped_over_100pct
FROM videos
GROUP BY length_bucket
ORDER BY MIN(duration_sec);

-- name: q3_weekday
-- Did the day I posted make a difference?
SELECT
    publish_weekday,
    COUNT(*)                 AS videos,
    ROUND(AVG(views), 0)     AS avg_views
FROM videos
GROUP BY publish_weekday
ORDER BY avg_views DESC;

-- name: q4_top_videos_share
-- How much of the channel came from the top 7 videos (~10% of the catalogue)?
WITH ranked AS (
    SELECT video, views, subs_gained,
           ROW_NUMBER() OVER (ORDER BY views DESC) AS view_rank
    FROM videos
)
SELECT
    ROUND(100.0 * SUM(CASE WHEN view_rank <= 7 THEN views END) / SUM(views), 1)             AS top7_pct_of_views,
    ROUND(100.0 * SUM(CASE WHEN view_rank <= 7 THEN subs_gained END) / SUM(subs_gained), 1) AS top7_pct_of_subs
FROM ranked;

-- name: q5_content_type
-- Which types of video performed best?
SELECT
    category,
    COUNT(*)                                                         AS videos,
    SUM(views)                                                       AS total_views,
    ROUND(100.0 * SUM(views) / (SELECT SUM(views) FROM videos), 1)   AS pct_of_views,
    ROUND(1000.0 * SUM(subs_gained) / SUM(views), 2)                 AS subs_per_1k_views,
    ROUND(AVG(avg_pct_viewed), 1)                                    AS avg_pct_viewed
FROM videos
GROUP BY category
ORDER BY total_views DESC;

-- name: q6_long_tail
-- Do the videos still get watched years after I stopped posting?
SELECT
    category,
    SUM(views_after_2019)                                              AS views_since_2020,
    ROUND(100.0 * SUM(views_after_2019) / SUM(views), 1)               AS pct_of_lifetime_views,
    SUM(CASE WHEN views_after_2019 > 0 THEN 1 ELSE 0 END)              AS videos_still_getting_views
FROM videos
GROUP BY category
ORDER BY pct_of_lifetime_views DESC;
