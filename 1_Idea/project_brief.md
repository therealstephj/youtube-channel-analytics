# Project Brief

## The situation
From **August 2011 to December 2019** I ran a YouTube channel. Like most creators, I made decisions on
gut feeling: what to make, how long to make it, when to post. This project goes back to the real data
to check which of those decisions actually mattered.

## The business question
> **What made some of my videos take off while others didn't, and what would I do differently if I started again?**

This is the same question any creator, social media team or marketing team asks:
*"Of everything we post, what actually works, and where should we put our effort?"*

## Who this analysis is for
- **A creator** deciding what to make next
- **A social/marketing team** deciding where to spend production time
- **A hiring manager** checking whether I can turn messy real-world data into decisions 🙂

## KPIs (how "performing well" is measured)

| KPI | Plain-English meaning | Why it matters |
|---|---|---|
| **Views** | How many times the video was watched | Reach |
| **Watch time (hours)** | Total time people spent watching | YouTube's algorithm rewards it |
| **Average view duration** | How long a typical viewer stayed | Whether the video holds attention |
| **Average % viewed** | How much of the video a typical viewer watched | Retention, fair across short and long videos |
| **Subscribers gained per 1,000 views** | How well a video turns viewers into fans | Long-term channel growth |
| **Likes & comments per 1,000 views** | How much viewers reacted | Engagement, fair across big and small videos |
| **Long-tail share** | % of a video's lifetime views that came after 2019 | Whether the content is "evergreen" |

Using **"per 1,000 views"** rates matters: a video with 100k views will always have more likes than one with
1k views. Rates make big and small videos comparable.

## Scope
- **In:** every public video published Aug 2011 – Dec 2019, from my own YouTube Studio export
- **Out:** other channels, paid promotion, anything the export doesn't include
- **Known gap:** YouTube only started reporting impressions and click-through rate (CTR) around 2019,
  so CTR can only be analyzed for the most recent videos, if at all.

## My predictions (written *before* looking at the data)
Writing these down first keeps the analysis honest. At the end I'll check which ones were right.

1. My **later videos** performed better than my early ones, because I got better at making them.
2. **Shorter videos** kept a higher % of viewers watching, but **longer videos** earned more total watch time.
3. **Posting day** made little difference.
4. A small number of videos (maybe the top 10%) brought in **most of the views and subscribers**.
5. Some old videos are **still getting views** years after I stopped posting.

*(These are draft predictions. Stephanie: edit them to your own gut feelings before Stage 2!)*

## Tools
Python (pandas, matplotlib) · SQL (SQLite) · Jupyter · Git/GitHub

## Plan

| Stage | Output |
|---|---|
| 1. Idea | This brief |
| 2. Data | Raw export + data dictionary (what every column means) |
| 3. Clean | Clean dataset + a log of every cleaning rule and how many rows it affected |
| 4. Analyze | Answers to the six questions, in Python and SQL |
| 5. Visualize | One clear chart per question |
| 6. Report | Final KPIs, findings vs predictions, recommendations |
