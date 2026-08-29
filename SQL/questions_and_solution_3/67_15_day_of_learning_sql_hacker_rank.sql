-- question statement
    -- For each contest day, find the number of "unique" submitters
    -- (hackers who have submitted on EVERY day since the contest
    -- began -- not new/sporadic submitters) and the hacker_id who
    -- made the most submissions that day (considering ALL hackers,
    -- not just the continuous ones). Ties on most-submissions go to
    -- the smaller hacker_id.

-- create table statement
CREATE TABLE Submissions (
    submission_date DATE,
    submission_id  INT PRIMARY KEY,
    hacker_id      INT,
    score          INT
);


-- Insert data
INSERT INTO Submissions (submission_date, submission_id, hacker_id, score) VALUES
('2016-03-01', 8494, 20703, 0),
('2016-03-01', 22403, 53473, 15),
('2016-03-01', 23965, 79722, 60),
('2016-03-01', 30173, 36396, 70),
('2016-03-02', 34928, 20703, 0),
('2016-03-02', 38740, 15758, 60),
('2016-03-02', 42769, 79722, 25),
('2016-03-02', 44364, 79722, 60),
('2016-03-03', 45440, 20703, 0),
('2016-03-03', 49050, 36396, 70),
('2016-03-03', 50273, 79722, 5),
('2016-03-04', 50344, 20703, 0),
('2016-03-04', 51360, 44065, 90),
('2016-03-04', 54404, 53473, 65),
('2016-03-04', 61533, 79722, 15),
('2016-03-05', 72852, 20703, 0),
('2016-03-05', 74546, 38289, 0),
('2016-03-05', 76487, 62529, 0),
('2016-03-05', 82439, 36396, 10),
('2016-03-05', 90006, 36396, 40),
('2016-03-06', 90404, 20703, 0);


-- Input data
"submission_date","submission_id","hacker_id","score"
2016-03-01,8494,20703,0
2016-03-01,22403,53473,15
2016-03-01,23965,79722,60
2016-03-01,30173,36396,70
2016-03-02,34928,20703,0
2016-03-02,38740,15758,60
2016-03-02,42769,79722,25
2016-03-02,44364,79722,60
... (full data as inserted)


-- Required Output (verified: executed against sqlite3, cross-checked
-- by hand-tracing every hacker's daily streak)
"submission_date","unique_cnt","hacker_id"
2016-03-01,4,20703
2016-03-02,2,79722
2016-03-03,2,20703
2016-03-04,2,20703
2016-03-05,1,36396
2016-03-06,1,20703

-- reasoning, day by day:
-- 03-01: everyone's first day -> all 4 hackers are "continuous" ->
--         unique_cnt=4. Everyone submitted once -> tie on hacker_id
--         -> 20703 wins (smallest).
-- 03-02: 15758 is a NEW hacker (first appearance) -> excluded from
--         unique_cnt. 20703 and 79722 have submitted every day so
--         far -> unique_cnt=2. 79722 submitted TWICE this day
--         (rows 42769, 44364) -> wins on submission count (2 vs 1).
-- 03-03: 36396 skipped day 2 -> streak broken, excluded. 20703 and
--         79722 still continuous -> unique_cnt=2. All tied at 1
--         submission -> 20703 wins (smallest id).
-- 03-04: 44065 is new; 53473 skipped days 2-3 (streak broken) ->
--         both excluded. unique_cnt=2 (20703, 79722). Tied at 1 ->
--         20703 wins.
-- 03-05: 38289, 62529 are new; 36396 had already skipped days 2 and
--         4, so even though they submit today, it's only their 3rd
--         distinct day out of 5 -> streak broken, excluded.
--         unique_cnt=1 (just 20703). 36396 submits TWICE this day
--         (rows 82439, 90006) -> wins on submission count.
-- 03-06: only 20703 submits, 6th day in a row -> unique_cnt=1,
--         wins by default.


--Solution steps
-- 1. Aggregate to one row per (submission_date, hacker_id), counting
--    how many submissions that hacker made that day (submission_cont)
--    -- this handles hackers who submit multiple times in one day.
-- 2. submission_day = dense_rank() of the date itself -- i.e. "this
--    is contest day N overall" (1st distinct date, 2nd, etc).
-- 3. user_submission_count = row_number() per hacker ordered by date
--    -- i.e. "this is the Nth distinct day THIS hacker has ever
--    submitted."
-- 4. The key trick: if submission_day == user_submission_count for a
--    given row, that hacker has submitted on every single day since
--    the contest started, with zero gaps -- if they'd ever missed a
--    day, their personal count would permanently lag behind the
--    global day count from that point on. This is the gaps-and-
--    islands pattern applied to "has this entity been present on
--    every step so far," rather than the more common "find runs of
--    consecutive rows."
-- 5. Sum that match-flag per submission_date to get unique_cnt --
--    correctly counting only continuous, non-new submitters, exactly
--    as the requirement specifies.
-- 6. Separately, rank ALL hackers (not just continuous ones) per day
--    by submission_cont desc, tie-broken by hacker_id ascending, and
--    keep rank = 1 to get that day's top submitter.

--SQL solution
with cte as (
    select
        submission_date,
        hacker_id,
        count(submission_id) as submission_cont,
        dense_rank() over (order by submission_date) as submission_day,
        row_number() over (partition by hacker_id order by submission_date) as user_submission_count
    from Submissions
    group by submission_date, hacker_id
),
day_counter as (
    select
        *,
        rank() over (partition by submission_date order by submission_cont desc, hacker_id) as submission_rank,
        sum(case when submission_day = user_submission_count then 1 else 0 end)
            over (partition by submission_date) as unique_cnt
    from cte
)
select submission_date, unique_cnt, hacker_id
from day_counter
where submission_rank = 1
order by submission_date;