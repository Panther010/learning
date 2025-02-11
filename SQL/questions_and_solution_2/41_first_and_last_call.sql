-- question statement
    -- Write an SQL to get the quite students in the class. Quite students are:
        -- Who tok at least one exam and did not score high score nor the low score in any on the exam.
        -- Do not return the student who have not given any exam.

-- create table statement
create table phone_log(caller_id int, recipient_id int, date_called timestamp);

-- Insert data
insert into phone_log(caller_id, recipient_id, date_called)
values(1, 2, '2019-01-01 09:00:00.000'),
       (1, 3, '2019-01-01 17:00:00.000'),
       (1, 4, '2019-01-01 23:00:00.000'),
       (2, 5, '2019-07-05 09:00:00.000'),
       (2, 3, '2019-07-05 17:00:00.000'),
       (2, 3, '2019-07-05 17:20:00.000'),
       (2, 5, '2019-07-05 23:00:00.000'),
       (2, 3, '2019-08-01 09:00:00.000'),
       (2, 3, '2019-08-01 17:00:00.000'),
       (2, 5, '2019-08-01 19:30:00.000'),
       (2, 4, '2019-08-02 09:00:00.000'),
       (2, 5, '2019-08-02 10:00:00.000'),
       (2, 5, '2019-08-02 10:45:00.000'),
       (2, 4, '2019-08-02 11:00:00.000'),
       (2, 3, '2019-08-03 09:00:00.000');

-- Input data
"caller_id","recipient_id","date_called"
1,2,2019-01-01 09:00:00.000
1,3,2019-01-01 17:00:00.000
1,4,2019-01-01 23:00:00.000
2,5,2019-07-05 09:00:00.000
2,3,2019-07-05 17:00:00.000
2,3,2019-07-05 17:20:00.000
2,5,2019-07-05 23:00:00.000
2,3,2019-08-01 09:00:00.000
2,3,2019-08-01 17:00:00.000
2,5,2019-08-01 19:30:00.000
2,4,2019-08-02 09:00:00.000
2,5,2019-08-02 10:00:00.000
2,5,2019-08-02 10:45:00.000
2,4,2019-08-02 11:00:00.000
2,3,2019-08-03 09:00:00.000

-- Required Output
"caller_id","recipient_id","call_date","min","max"
2,4,2019-08-02,2019-08-02 09:00:00.000,2019-08-02 11:00:00.000
2,5,2019-07-05,2019-07-05 09:00:00.000,2019-07-05 23:00:00.000

--Solution steps
-- 1. calculate the date from the date_called column
-- 2. using first_value rank function get the first and last recipient_id
-- 3. save this data to temp table
-- 4. Apply filter to get records where first recipient_id = last recipient_id and recipient_id = first recipient_id
-- 5. now group by all the column get the min and max date_called
-- 6. In case want t avoid single call records use having clause min(date_called) != max(date_called)


--SQL solution1
with cte as (
	select
		*,
		date(date_called) as call_date,
		first_value(recipient_id) over(partition by caller_id, date(date_called) order by date_called) as first_call,
		first_value(recipient_id) over(partition by caller_id, date(date_called) order by date_called desc) as last_call
	from phonelog)
select
	caller_id,
	recipient_id,
	call_date,
	min(date_called),
	max(date_called)
from cte
where first_call = last_call and first_call = recipient_id
group by caller_id,
	recipient_id,
	call_date
having min(date_called) != max(date_called)