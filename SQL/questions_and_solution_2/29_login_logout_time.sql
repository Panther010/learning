-- question statement
    -- Find out login and logout time with continuous time worked

-- create table statement
create table event_status (event_time varchar(10), status varchar(10));


-- Insert data
insert into event_status values
('10:01','on'),
('10:02','on'),
('10:03','on'),
('10:04','off'),
('10:07','on'),
('10:08','on'),
('10:09','off')
,('10:11','on'),
('10:12','off');


-- Input data
"event_time","status"
"10:01",on
"10:02",on
"10:03",on
"10:04",off
"10:07",on
"10:08",on
"10:09",off
"10:11",on
"10:12",off


-- Required Output
"login","logout","time_count"
"10:01","10:04",3
"10:07","10:09",2
"10:11","10:12",1



--Solution steps
-- 1. Get previous status using lag and create a temp table
-- 2. From this temp table check id current status is on and previous was off
-- 3. This combination indicate new series
-- 4. Create different group key by passing 1 for this case and sum these values
-- 5. Get the max and min event_time to get login and logout
-- 6. count() group key - 1 to get count group by group key

--SQL solution1
with prev_status_col as (
	select
		*,
		lag(status,1,status) over(order by event_time) as prev_status
	from event_status),
group_key_tbl as (
	select
		*,
		sum(case when status = 'on' and prev_status = 'off' then 1 else 0 end) over(order by event_time) as group_key
	from prev_status_col)

select
	min(event_time) as login,
	max(event_time) as logout,
	count(group_key) - 1 as time_count
from group_key_tbl
group by group_key


--SQL solution2
with cte as(
	select
		event_time,
		status,
		cast(right(event_time,2) as integer) - rank() over( order by event_time) as rnk_id
	from event_status)
select
	min(event_time),
	max(event_time),
	count(rnk_id) - 1 as cnt
from cte
group by rnk_id
order by min(event_time)