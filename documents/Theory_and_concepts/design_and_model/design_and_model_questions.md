# OLAP Backend Design: Social Media Reactions — Interview Notes

## The Question
Design a backend (OLAP) for a social media platform where users post photos and others react with emojis (like, love, haha, angry, etc).

**Requirements:**
1. Track number and type of reactions per post
2. Users can change or remove their reaction
3. Analyze trends (most-reacted post, top emojis, daily activity)
4. **Target query:** For each of the past 7 days, list the top 3 emojis used by users from California, on posts created by influencers (≥100k followers) — with total reaction count and distinct post count.

---
### Ask question:
- Scale & Performance SLAs (The "How Big?" Questions)
  - What is the expected scale of daily data ingestion? (e.g., How many posts per day? How many reactions per second during peak hours?)
- When a user changes or removes their reaction, do we need a full audit trail (historical history of every click/change), or do we only care about the current active state?

## Schema

### Dimension Tables
| Table           | Key Fields                                                     | Notes                                   |
|-----------------|----------------------------------------------------------------|-----------------------------------------|
| `dim_user`      | user_id (PK), name, location_id (FK), created_at               | **SCD Type 2** — location can change    |
| `dim_location`  | location_id (PK), city, state, country                         | Enables `state = 'California'` filter   |
| `dim_emoji`     | emoji_id (PK), name, description                               | Append-only, no SCD needed              |
| `dim_date`      | date_id (PK), date, day, week, month                           | Standard date dim                       |
| `dim_post`      | post_id (PK), user_id (FK), post_type, description, created_at | Date-partitioned; effectively immutable |
| `dim_influence` | user_id, date_id, follower_count                               | **Daily snapshot**, not live-computed   |

### Fact Tables
| Table                            | Key Fields                                                                              | Notes                                                                |
|----------------------------------|-----------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| `fact_follow`                    | follower_id, followed_id, created_at                                                    | This is a **fact**, not a dim (relationship log)                     |
| `fact_reaction` (event log)      | reaction_id, post_id, reactor_id, emoji_id, action_type (add/change/remove), created_at | **Append-only**, immutable — source of truth for trends              |
| `current_reaction` (state table) | reactor_id, post_id, emoji_id, updated_at                                               | Small mutable upsert table — "what is the reaction right now"        |
| `agg_daily_post_emoji`           | post_id, emoji_id, date_id, reaction_count                                              | **Pre-aggregated rollup**, refreshed nightly, for fast trend queries |

---

## Key Design Decisions

1. **Reactions are mutable → split into two tables.**
   - Event log (append-only, `action_type`) for historical/trend analysis.
   - Current-state table (upsert) for "what's the reaction now" lookups.
   - Don't try to upsert a partitioned fact table directly — name this as a deliberate two-table pattern.

2. **Resolve the ambiguity explicitly:** trend queries should use the *event log as of that day* (what happened), not current state — otherwise historical counts shift every time someone changes a reaction. State this assumption up front in an interview.

3. **Influencer status = daily snapshot table**, not a live COUNT(*) against a followers table — avoids expensive joins at query time.

4. **SCD Type 2 only where it matters** — `dim_user` (location changes). Don't blanket-apply it to immutable dims like `dim_post`/`dim_emoji`.

5. **Pre-aggregation layer is the classic OLAP move** — don't aggregate raw `fact_reaction` on every dashboard query; roll up nightly into `agg_daily_post_emoji`.

6. **Partitioning/clustering:** partition `dim_post` and fact tables by date; cluster `fact_reaction` by `(date, post_id)` to serve both "trending post" and "per-post" query patterns.

---

## Query Sketch (target requirement #4)

```sql
WITH ca_reactions AS (
  SELECT r.emoji_id, r.post_id, d.date_id
  FROM fact_reaction r
  JOIN dim_user u ON r.reactor_id = u.user_id
  JOIN dim_location l ON u.location_id = l.location_id
  JOIN dim_post p ON r.post_id = p.post_id
  JOIN dim_influence i ON p.user_id = i.user_id AND i.date_id = r.date_id
  JOIN dim_date d ON r.date_id = d.date_id
  WHERE l.state = 'California'
    AND i.follower_count >= 100000
    AND d.date >= CURRENT_DATE - 7
),
ranked AS (
  SELECT date_id, emoji_id,
         COUNT(*) AS reaction_count,
         COUNT(DISTINCT post_id) AS distinct_posts,
         ROW_NUMBER() OVER (PARTITION BY date_id ORDER BY COUNT(*) DESC) AS rnk
  FROM ca_reactions
  GROUP BY date_id, emoji_id
)
SELECT * FROM ranked WHERE rnk <= 3;
```

---



Que 2 Design a warehouses for real time data
working for stock exchange 
getting millisecond changes
very high throughput data
ingest real time data build pipeline and create stream analysis. Analyse realtime analytics and ware house