-- question statement
    -- to find second most recent activity and if user has only 1 activity then return that as it is

-- create table statement
create table user_activity(username varchar(20), activity varchar(20), start_date Date, end_date Date);

-- Insert data
insert into user_activity values
    ('Alice','Travel','2020-02-12','2020-02-20')
    ,('Alice','Dancing','2020-02-21','2020-02-23')
    ,('Alice','Travel','2020-02-24','2020-02-28')
    ,('Bob','Travel','2020-02-11','2020-02-18');

-- Input data
--table 1 transactions:
"username","activity","start_date","end_date"
Alice,Travel,2020-02-12,2020-02-20
Alice,Dancing,2020-02-21,2020-02-23
Alice,Travel,2020-02-24,2020-02-28
Bob,Travel,2020-02-11,2020-02-18

-- Required Output
"username","activity","start_date","end_date"
Alice,Dancing,2020-02-21,2020-02-23
Bob,Travel,2020-02-11,2020-02-18

--Solution steps
    --calculate ranking and count using window function and apply the required filter

--SQL solution1
with activity_cal as (
    select
        *,
        rank() over(partition by username order by start_date) as activity_rank,
        count(activity) over(partition by username) as activity_count
    from UserActivity)
select
    username,
    activity,
    start_date,
    end_date
from activity_cal
where
	(activity_count > 2 and activity_rank = 2)
	or activity_count = 1

--Additional logics Recursive CTE sample
