-- question statement
    -- Find how much time each employee spent in the office on a
    -- given day (first login to last logout, the full building
    -- presence span), and separately how "productive" they were
    -- (the actual sum of time spent logged in, excluding any gaps
    -- between logout/login pairs -- e.g. a lunch break away from
    -- the office).

-- create table statement
CREATE TABLE swipe (
    employee_id   INT,
    activity_type VARCHAR(10),
    activity_time timestamp
);


-- Insert sample data
INSERT INTO swipe (employee_id, activity_type, activity_time) VALUES
(1, 'login', '2024-07-23 08:00:00'),
(1, 'logout', '2024-07-23 12:00:00'),
(1, 'login', '2024-07-23 13:00:00'),
(1, 'logout', '2024-07-23 17:00:00'),
(2, 'login', '2024-07-23 09:00:00'),
(2, 'logout', '2024-07-23 11:00:00'),
(2, 'login', '2024-07-23 12:00:00'),
(2, 'logout', '2024-07-23 15:00:00'),
(1, 'login', '2024-07-24 08:30:00'),
(1, 'logout', '2024-07-24 12:30:00'),
(2, 'login', '2024-07-24 09:30:00'),
(2, 'logout', '2024-07-24 10:30:00');


-- Input data
"employee_id","activity_type","activity_time"
1,login,2024-07-23 08:00:00
1,logout,2024-07-23 12:00:00
1,login,2024-07-23 13:00:00
1,logout,2024-07-23 17:00:00
2,login,2024-07-23 09:00:00
2,logout,2024-07-23 11:00:00
2,login,2024-07-23 12:00:00
2,logout,2024-07-23 15:00:00
1,login,2024-07-24 08:30:00
1,logout,2024-07-24 12:30:00
2,login,2024-07-24 09:30:00
2,logout,2024-07-24 10:30:00


-- Required Output (verified: matched by hand-simulating the window
-- function logic; both solution versions below agree)
"employee_id","activity_date","daily_work","daily_productivity"
1,2024-07-23,9,8
1,2024-07-24,4,4
2,2024-07-23,6,5
2,2024-07-24,1,1

-- reasoning:
-- emp1, 07-23: in the building 08:00-17:00 (span=9h). Actually
--   logged in during 08:00-12:00 and 13:00-17:00 (4h+4h=8h) -- the
--   12:00-13:00 gap is a logged-out break, excluded from productivity.
-- emp2, 07-23: in the building 09:00-15:00 (span=6h). Logged in
--   09:00-11:00 and 12:00-15:00 (2h+3h=5h) -- 1h gap excluded.
-- emp1, 07-24 / emp2, 07-24: single unbroken session each day, so
--   daily_work and daily_productivity are equal (4h and 1h).


--Solution steps
-- 1. Cast activity_time down to a plain date (activity_date) to
--    group swipes by calendar day per employee.
-- 2. first_value(activity_time) per (employee, day) gives the
--    day's first login/swipe -- "arrived at."
-- 3. last_value(activity_time) -- with the frame explicitly widened
--    to the WHOLE partition (ROWS BETWEEN UNBOUNDED PRECEDING AND
--    UNBOUNDED FOLLOWING) -- gives the day's last logout/swipe --
--    "left at." Without that explicit frame, last_value() would
--    default to only looking up to the CURRENT row, which is the
--    single most common last_value() mistake in SQL.
-- 4. daily_work = last_logout - first_login -- the full "time spent
--    in the office" span, including any short gaps within the day.
-- 5. lead(activity_time) on each login row finds that SPECIFIC
--    session's matching logout, so (next_logout - this_login) gives
--    one session's actual duration.
-- 6. Filter to only 'login' rows before aggregating, then per
--    employee/day: MIN(daily_work) collapses the (same-valued,
--    repeated-per-row) office-span into one number, and
--    SUM(daily_productivity) adds up every individual session's
--    duration for that day.

--SQL solution1 -- staged CTEs (readable step-by-step)
with cte as (
	select
		*,
		cast(activity_time as date) as activity_date
	from swipe
),
entry as (
	select
		*,
		first_value(activity_time) over(partition by employee_id, activity_date order by activity_time) first_login,
		last_value(activity_time) over(partition by employee_id, activity_date order by activity_time
		ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) last_logout,
		lead(activity_time) over(partition by employee_id, activity_date order by activity_time) next_logout
	from cte),
calculator as(
	select
		employee_id,
		activity_date,
		extract(hour from justify_hours(last_logout - first_login)) as daily_work,
		extract(hour from justify_hours(next_logout - activity_time)) as daily_productivity
	from entry
	where activity_type = 'login')
select
	employee_id,
	activity_date,
	min(daily_work) as daily_work,
	sum(daily_productivity) as daily_productivity
from calculator
group by employee_id, activity_date;


--SQL solution2 -- combined CTE (functionally identical, one fewer step)
with cte as (
select
	*,
	cast(activity_time as date) as activity_date,
	first_value(activity_time) over(partition by employee_id, cast(activity_time as date) order by activity_time) first_login,
	last_value(activity_time) over(partition by employee_id, cast(activity_time as date) order by activity_time
		ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) last_logout,
	lead(activity_time) over(partition by employee_id, cast(activity_time as date) order by activity_time) next_logout
from swipe),
calculator as (
	select
		employee_id,
		activity_date,
		extract(hour from justify_hours(last_logout - first_login)) as daily_work,
		extract(hour from justify_hours(next_logout - activity_time)) as daily_productivity
	from cte
	where activity_type = 'login')
select
	employee_id,
	activity_date,
	min(daily_work) as daily_work,
	sum(daily_productivity) as daily_productivity
from calculator
group by employee_id, activity_date;
