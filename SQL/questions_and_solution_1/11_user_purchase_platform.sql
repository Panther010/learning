-- question statement
    -- The table logs the spending's history of users that make purchases from an online shopping website which has a desktop
        --and a mobile application.
    -- Write an SQL query to find the total number of users and the total amount spent using mobile only, desktop only
        --and both mobile and desktop together for each date.

-- create table statement
create table spending (user_id int, spend_date date, platform varchar(10), amount int);

-- Insert data
insert into spending values
    (1,'2019-07-01','mobile',100),
    (1,'2019-07-01','desktop',100),
    (2,'2019-07-01','mobile',100),
    (2,'2019-07-02','mobile',100),
    (3,'2019-07-01','desktop',100),
    (3,'2019-07-02','desktop',100);


-- Input data
--table 1 spending:
"user_id","spend_date","platform","amount"
1,2019-07-01,mobile,100
1,2019-07-01,desktop,100
2,2019-07-01,mobile,100
3,2019-07-01,desktop,100
2,2019-07-02,mobile,100
3,2019-07-02,desktop,100

-- Required Output
"spend_date","platform","total_amount","total_users"
2019-07-01,mobile,100,1
2019-07-01,desktop,100,1
2019-07-01,both,200,1
2019-07-02,mobile,100,1
2019-07-02,desktop,100,1
2019-07-02,both,0,0

--Solution steps
    --calculate the total amount for usr with one platform only
    --calculate total amount for user using both the platform and union both the result
    --while union add distinct record for both and 0 as well with null user id and 0 total
    --calculate total user each day by grouping on  the result of above cte

--SQL solution1
with cte as(
    select spend_date, user_id, max(platform) as platform, sum(amount) as amount
        from spending
        group by spend_date, user_id
        having count(platform) = 1
    union all
    select spend_date, user_id, 'both' as platform, sum(amount) as amount
        from spending
        group by spend_date, user_id
        having count(platform) = 2
    union all
    select distinct spend_date, null::bigint as user_id, 'both' as platform, 0 as amount
    from spending s)
select spend_date, platform, sum(amount) as total_amount, count(distinct user_id) as total_users
from cte co
group by spend_date, platform
order by spend_date, platform desc

--Additional logics Not getting 0 row
with daily_uses as (
	select
		user_id,
		spend_date,
		count(1) as daily_use_by_user,
		sum(amount) as total_amount
	from spending
	group by user_id, spend_date),
update_platform as(
	select
		a.user_id,
		a.spend_date,
		case when b.daily_use_by_user = 2 then 'both' else a.platform end as platform,
		b.total_amount
	from spending a inner join daily_uses b on
		a.user_id = b.user_id and
		a.spend_date = b.spend_date)
select
	spend_date,
	platform,
	total_amount,
	count(1) as total_user
from update_platform
group by spend_date, platform, total_amount

--Additional logic:
with spend_agg as (
	select
		user_id, spend_date,
		string_agg(distinct platform, '|') platform,
		sum(amount) total_amount,
		count(1) total_users
		from spending
	group by user_id, spend_date)
select
	spend_date,
	case when platform like '%|%' then 'both' else platform end as platform,
	total_amount,
	total_users
from spend_agg
order by spend_date
