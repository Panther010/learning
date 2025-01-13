-- question statement
    -- write a query to calculate conversation rate or the users who
        -- join prime member with in 30 days of joining
        -- and are music users

-- create table statement
create table users
(
user_id integer,
name varchar(20),
join_date date
);


create table events
(
user_id integer,
type varchar(10),
access_date date
);



-- Insert data
insert into users
values (1, 'Jon', CAST('2020-02-14' AS date)),
(2, 'Jane', CAST('2020-02-14' AS date)),
(3, 'Jill', CAST('2020-02-15' AS date)),
(4, 'Josh', CAST('2020-02-15' AS date)),
(5, 'Jean', CAST('2020-02-16' AS date)),
(6, 'Justin', CAST('2020-02-17' AS date)),
(7, 'Jeremy', CAST('2020-02-18' AS date));

insert into events values
(1, 'Pay', CAST('2020-03-01' AS date)),
(2, 'Music', CAST('2020-03-02' AS date)),
(2, 'P', CAST('2020-03-12' AS date)),
(3, 'Music', CAST('2020-03-15' AS date)),
(4, 'Music', CAST('2020-03-15' AS date)),
(1, 'P', CAST('2020-03-16' AS date)),
(3, 'P', CAST('2020-03-22' AS date));
-- Input data
--table 1 orders:
"order_id","customer_id","product_id"
1,1,1
1,1,2
1,1,3
2,2,1
2,2,2
2,2,4
3,1,5

--table 2 orders:
"id","name"
1,A
2,B
3,C
4,D
5,E

-- Required Output
"total_users","prim_music","conversion_rate"
3,1,0.33333333333333333333

--Solution steps
    --calculate total prime users
    --apply filter for Music users
    --calculate the sum of users who subscribed prime with in 30 days of their joining
    --get the ratio of these two columns to get the conversion rate

--SQL solution1
select
    sum(case when e.access_date - u.join_date < 30 then 1 else 0 end) as prim_music,
    count(1) as total_users,
    sum(case when e.access_date - u.join_date < 30 then 1 else 0 end) * 1.0 / count(1) as conversion_rate
from
    users u left join
    events e on u.user_id = e.user_id and e.type = 'P'
where
    u.user_id in (select user_id from events where type = 'Music')

--Additional logics Recursive CTE sample
