-- question statement
    -- write a sql queries to solve below questions
        --  1. Find active users each day
        --  2. Find active user each week
        --  3. Find total users who made purchase same day they installed the app
        --  4. Percentage of paid users in India, USA and any other country should be tagged as Others
        --  5. Among all te users who installed the app on the next day and purchased on very next day

-- create table statement
CREATE table activity (user_id varchar(20), event_name varchar(20), event_date date, country varchar(20));

-- Insert data
insert into activity values (1,'app-installed','2022-01-01','India')
    ,(1,'app-purchase','2022-01-02','India')
    ,(2,'app-installed','2022-01-01','USA')
    ,(3,'app-installed','2022-01-01','USA')
    ,(3,'app-purchase','2022-01-03','USA')
    ,(4,'app-installed','2022-01-03','India')
    ,(4,'app-purchase','2022-01-03','India')
    ,(5,'app-installed','2022-01-03','SL')
    ,(5,'app-purchase','2022-01-03','SL')
    ,(6,'app-installed','2022-01-04','Pakistan')
    ,(6,'app-purchase','2022-01-04','Pakistan');

-- Input data
--table 1 activity:
"user_id","event_name","event_date","country"
"1",app-installed,2022-01-01,India
"1",app-purchase,2022-01-02,India
"2",app-installed,2022-01-01,USA
"3",app-installed,2022-01-01,USA
"3",app-purchase,2022-01-03,USA
"4",app-installed,2022-01-03,India
"4",app-purchase,2022-01-03,India
"5",app-installed,2022-01-03,SL
"5",app-purchase,2022-01-03,SL
"6",app-installed,2022-01-04,Pakistan
"6",app-purchase,2022-01-04,Pakistan


-- Required Output

    --Que.   1 Find active users each day
"event_date","count"
2022-01-01,3
2022-01-02,1
2022-01-03,3
2022-01-04,1

    --Que.   2 Find active user each week
"event_week","user_id"
1.0,4
52.0,3

    --Que.  3 Find total users who made purchase same day they installed the app
"event_date","same_day_purchase_count"
2022-01-01,0
2022-01-02,0
2022-01-03,2
2022-01-04,1

    --Que.  4. Percentage of paid users in India, USA and any other country should be tagged as Others
"country","activ_percentage"
India,40.0000000000000000
Others,40.0000000000000000
USA,20.0000000000000000

    --Que 5.    Among all te users who installed the app on the next day and purchased on very next day
"event_date","user_count"
2022-01-01,0
2022-01-02,1
2022-01-03,0
2022-01-04,0


--Solution steps

--SQL solution que 1
select
    event_date,
    count(distinct user_id) from activity
group by event_date

--SQL solution que 2
select
    date_part('week', event_date) as event_week,
    count(distinct user_id) as user_id
from activity
group by date_part('week', event_date)

--SQL solution que 3
select
	a.event_date,
	sum(case when a.event_date = b.event_date then 1 else 0 end) as same_day_purchase_count
from activity a left join activity b
	on a.user_id = b.user_id
	and a.event_name = 'app-installed'
	and b.event_name = 'app-purchase'
group by a.event_date
order by a.event_date

--SQL solution que 4
with country_user as (
	select
		case when country in ('USA', 'India') then country else 'Others' end as country,
		count(country) as user_count
	from activity
	where event_name = 'app-purchase'
	group by case when country in ('USA', 'India') then country else 'Others' end)
select
    country,
    user_count * 100 * 1.0 /sum(user_count) over() as activ_percentage
from country_user

--SQL solution que 5
with next_dat_purchase as (
	select
		event_date,
		lag(event_date) over(partition by user_id order by event_date) as purchase_date,
		event_date - lag(event_date) over(partition by user_id order by event_date) as date_difference
	from activity)
select
    event_date,
	sum(case when date_difference = 1 then 1 else 0 end) as user_count
from next_dat_purchase
group by event_date
order by event_date

--Additional logics Recursive CTE sample
