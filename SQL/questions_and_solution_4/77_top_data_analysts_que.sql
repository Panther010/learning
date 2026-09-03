-- question statement
    -- Identify user sessions: a session is a sequence of a user's
    -- events where consecutive events are <= 30 minutes apart. A
    -- gap of more than 30 minutes starts a new session. Return
    -- session_id, session_start_time, session_end_time, and
    -- session_duration per session.

-- create table statement
create table events (
    userid     int,
    event_type varchar(20),
    event_time timestamp
);


-- Insert data
insert into events VALUES (1, 'click', '2023-09-10 09:00:00');
insert into events VALUES (1, 'click', '2023-09-10 10:00:00');
insert into events VALUES (1, 'scroll', '2023-09-10 10:20:00');
insert into events VALUES (1, 'click', '2023-09-10 10:50:00');
insert into events VALUES (1, 'scroll', '2023-09-10 11:40:00');
insert into events VALUES (1, 'click', '2023-09-10 12:40:00');
insert into events VALUES (1, 'scroll', '2023-09-10 12:50:00');
insert into events VALUES (2, 'click', '2023-09-10 09:00:00');
insert into events VALUES (2, 'scroll', '2023-09-10 09:20:00');
insert into events VALUES (2, 'click', '2023-09-10 10:30:00');


-- Input data
"userid","event_type","event_time"
1,click,2023-09-10 09:00:00
1,click,2023-09-10 10:00:00
1,scroll,2023-09-10 10:20:00
1,click,2023-09-10 10:50:00
1,scroll,2023-09-10 11:40:00
1,click,2023-09-10 12:40:00
1,scroll,2023-09-10 12:50:00
2,click,2023-09-10 09:00:00
2,scroll,2023-09-10 09:20:00
2,click,2023-09-10 10:30:00


-- Required Output (verified: executed with exact integer-second
-- precision, matches full hand-trace)
"userid","session_id","session_start_time","session_end_time","session_duration","event_count"
1,1,2023-09-10 09:00:00,2023-09-10 09:00:00,0,1
1,2,2023-09-10 10:00:00,2023-09-10 10:50:00,50,3
1,3,2023-09-10 11:40:00,2023-09-10 11:40:00,0,1
1,4,2023-09-10 12:40:00,2023-09-10 12:50:00,10,2
2,1,2023-09-10 09:00:00,2023-09-10 09:20:00,20,2
2,2,2023-09-10 10:30:00,2023-09-10 10:30:00,0,1

-- reasoning, user1:
-- 09:00 -> 10:00 is a 60-min gap -> new session -> 09:00 is a
--   lone 1-event session
-- 10:00 -> 10:20 (20 min) -> same session
-- 10:20 -> 10:50 (EXACTLY 30 min) -> still same session, since the
--   rule is "> 30 min starts new session" (30 itself doesn't qualify)
-- 10:50 -> 11:40 (50 min) -> new session -> 11:40 is a lone event
-- 11:40 -> 12:40 (60 min) -> new session
-- 12:40 -> 12:50 (10 min) -> same session


--Solution steps
-- 1. lag(event_time) per user gets the previous event's timestamp;
--    using the value itself as the default handles the first row
--    per user cleanly (diff becomes 0, never triggers a new session).
-- 2. extract(epoch from (event_time - lag)) / 60 converts the raw
--    interval into minutes.
-- 3. Flag a new session (1) whenever that gap exceeds 30 minutes,
--    else 0 -- classic gaps-and-islands boundary marker.
-- 4. A running sum of those flags (+1 to start numbering at 1
--    instead of 0) gives each event a session_id, per user.
-- 5. Group by (userid, session_id) and aggregate min/max event_time
--    for the session window, and count events per session.


--SQL solution
with cte as (
	select
		*,
		lag(event_time, 1, event_time) over(partition by userid order by event_time) as next_event,
		extract(EPOCH from (event_time - lag(event_time, 1, event_time) over(partition by userid order by event_time)))/60 as event_diff
	from events
),
new_session_window as (
	select
		*,
		case when event_diff > 30 then 1
		else 0 end as new_session
	from cte
),
session_window as (
	select
		*,
		sum(new_session) over(partition by userid order by event_time)+1 as session_id
	from new_session_window
)
select
	userid,
	session_id,
	min(event_time) as session_start_time,
	max(event_time) as session_end_time,
	extract(EPOCH from (max(event_time) - min(event_time)))/60 session_duration,
	count(event_type) as event_count
from session_window
group by userid, session_id
order by userid, session_id;

