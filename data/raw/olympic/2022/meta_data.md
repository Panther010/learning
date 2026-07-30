# Olympic Dataset — Reference Notes

Local path base: `/Users/bakulseth/PycharmProjects/learning/data/raw/olympic/2022/`

## Dataset Overview

| Table                  | Description                                                 |
|------------------------|-------------------------------------------------------------|
| `olympic_athletes.csv` | Personal information about athletes (name, short bio, etc.) |
| `olympic_medals.csv`   | General information on medalists (Athlete or Team)          |
| `olympic_hosts.csv`    | Host info (year, city, country, etc.)                       |
| `olympic_results.csv`  | General information on results (Athlete or Team)            |
| `olympic_results.pkl`  | Same as `olympic_results.csv`, saved as a pickle file       |

---

## 1. `olympic_athletes.csv`

**Schema**

| Column                 | Type   | Nullable |
|------------------------|--------|----------|
| `athlete_url`          | string | ✅        |
| `athlete_full_name`    | string | ✅        |
| `games_participations` | string | ✅        |
| `first_game`           | string | ✅        |
| `athlete_year_birth`   | string | ✅        |
| `athlete_medals`       | string | ✅        |
| `bio`                  | string | ✅        |

**Row counts (non-null) per column**

| Column                 | Count   |
|------------------------|---------|
| `athlete_url`          | 189,960 |
| `athlete_full_name`    | 95,919  |
| `games_participations` | 93,413  |
| `first_game`           | 90,726  |
| `athlete_year_birth`   | 85,827  |
| `athlete_medals`       | 25,420  |
| `bio`                  | 23,007  |

> ⚠️ **Data quality note:** These are string columns, but `.describe()` is computing numeric-looking stats (mean/stddev/percentiles) on them — meaning some rows have messy/misaligned data (e.g., a name field showing "200m freestyle...", a birth-year field showing "Zombie Apocalypse", bio text leaking into other columns). This strongly suggests **broken CSV parsing** — likely commas inside free-text fields (like `bio`) shifting values into the wrong columns. Worth re-checking the CSV read with a proper quote/escape character before trusting this table.

---

## 2. `olympic_hosts.csv`

**Schema**

| Column            | Type      | Nullable |
|-------------------|-----------|----------|
| `game_slug`       | string    | ✅        |
| `game_end_date`   | timestamp | ✅        |
| `game_start_date` | timestamp | ✅        |
| `game_location`   | string    | ✅        |
| `game_name`       | string    | ✅        |
| `game_season`     | string    | ✅        |
| `game_year`       | integer   | ✅        |

**Summary**
- **Total rows:** 53 (one per Olympic Games, Summer + Winter, 1896–2022)
- `game_year` → mean ≈ **1967.5**, min **1896**, max **2022**
- `game_season` → values: `Summer`, `Winter`
- Example range: `albertville-1992` (min slug) → `vancouver-2010` (max slug, alphabetically)

This table looks **clean** — no obvious parsing issues, sensible date/int types.

---

## 3. `olympic_medals.csv`

**Schema**

| Column                  | Type   | Nullable |
|-------------------------|--------|----------|
| `discipline_title`      | string | ✅        |
| `slug_game`             | string | ✅        |
| `event_title`           | string | ✅        |
| `event_gender`          | string | ✅        |
| `medal_type`            | string | ✅        |
| `participant_type`      | string | ✅        |
| `participant_title`     | string | ✅        |
| `athlete_url`           | string | ✅        |
| `athlete_full_name`     | string | ✅        |
| `country_name`          | string | ✅        |
| `country_code`          | string | ✅        |
| `country_3_letter_code` | string | ✅        |

**Row counts (non-null) per column**

| Column                  | Count  |
|-------------------------|--------|
| `discipline_title`      | 21,697 |
| `slug_game`             | 21,697 |
| `event_title`           | 21,697 |
| `event_gender`          | 21,697 |
| `medal_type`            | 21,697 |
| `participant_type`      | 21,697 |
| `participant_title`     | 6,584  |
| `athlete_url`           | 17,027 |
| `athlete_full_name`     | 18,073 |
| `country_name`          | 21,697 |
| `country_code`          | 20,200 |
| `country_3_letter_code` | 21,697 |

**Key value ranges**
- `medal_type`: `BRONZE`, `SILVER` (also expect `GOLD` — just didn't land as min/max alphabetically)
- `participant_type`: `Athlete`, `GameTeam`
- `discipline_title`: ranges from "3x3 Basketball" to "Wrestling"
- `country_name`: full range from Afghanistan → Zimbabwe (i.e., a genuinely global dataset)

This table looks **structurally clean** (counts match across most columns, no obviously misaligned values in min/max).

---

## 4. `olympic_results.csv`

**Schema**

| Column                  | Type   | Nullable |
|-------------------------|--------|----------|
| `discipline_title`      | string | ✅        |
| `event_title`           | string | ✅        |
| `slug_game`             | string | ✅        |
| `participant_type`      | string | ✅        |
| `medal_type`            | string | ✅        |
| `athletes`              | string | ✅        |
| `rank_equal`            | string | ✅        |
| `rank_position`         | string | ✅        |
| `country_name`          | string | ✅        |
| `country_code`          | string | ✅        |
| `country_3_letter_code` | string | ✅        |
| `athlete_url`           | string | ✅        |
| `athlete_full_name`     | string | ✅        |
| `value_unit`            | string | ✅        |
| `value_type`            | string | ✅        |

**Row counts (non-null) per column**

| Column                  | Count   |
|-------------------------|---------|
| `discipline_title`      | 162,804 |
| `event_title`           | 162,804 |
| `slug_game`             | 162,804 |
| `participant_type`      | 162,804 |
| `medal_type`            | 20,206  |
| `athletes`              | 7,976   |
| `rank_equal`            | 32,555  |
| `rank_position`         | 158,916 |
| `country_name`          | 162,804 |
| `country_code`          | 157,823 |
| `country_3_letter_code` | 162,802 |
| `athlete_url`           | 130,021 |
| `athlete_full_name`     | 141,666 |
| `value_unit`            | 78,649  |
| `value_type`            | 90,039  |

_> ⚠️ **Data quality note:** Same issue as `olympic_athletes.csv` — the `.describe()` output shows clearly broken values (e.g., `rank_position` showing text like `"(""Claude N'GORAN"""`, `country_code` showing `"None)]"`, `athlete_full_name` showing `"DENI DENI"` in a min slot, `value_unit` showing `"same time"`). This is a strong sign that the **`athletes` column contains a stringified list of tuples** (e.g., `"[('Alex O'BRIEN', ...)]"`) with embedded commas and quotes, which is **breaking the CSV parser** and shifting values across columns for a subset of rows._
>
> **Recommendation:** Re-read this file with a robust CSV parser (proper `quote`/`escape` handling, or treat `athletes` as a single quoted JSON-like string field) before running further analysis — a chunk of `rank_position`, `country_code`, `athlete_full_name`, and `value_unit`/`value_type` values are likely misaligned in the current load.

---

## Overall Takeaways

- **Clean tables:** `olympic_hosts.csv`, `olympic_medals.csv`
- **Tables needing a parsing fix:** `olympic_athletes.csv`, `olympic_results.csv` — both show signs of free-text/list fields (`bio`, `athletes`) leaking commas/quotes into neighboring columns.
- **Next step before analysis:** Re-load the two problematic CSVs with correct quoting rules (e.g., `quote='"'`, `escape='"'`, or `multiLine=True` in Spark's CSV reader) and re-run `.describe()` to confirm the counts and value ranges look sane.

