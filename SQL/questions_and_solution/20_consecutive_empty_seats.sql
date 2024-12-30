-- question statement
    -- write a sql to find consecutive 3 or more empty seats

-- create table statement
create table bms (seat_no int ,is_empty varchar(10));


-- Insert data
insert into bms values
    (1,'N')
    ,(2,'Y')
    ,(3,'N')
    ,(4,'Y')
    ,(5,'Y')
    ,(6,'Y')
    ,(7,'N')
    ,(8,'Y')
    ,(9,'Y')
    ,(10,'Y')
    ,(11,'Y')
    ,(12,'N')
    ,(13,'Y')
    ,(14,'Y');

-- Input data
--table 1 bms:
"seat_no","is_empty"
1,N
2,Y
3,N
4,Y
5,Y
6,Y
7,N
8,Y
9,Y
10,Y
11,Y
12,N
13,Y
14,Y

-- Required Output
"seat_no","is_empty"
4,Y
5,Y
6,Y
8,Y
9,Y
10,Y
11,Y



--Solution steps

--SQL solution 1 using row_number function
with empty_seats as (
	select
	*,
	row_number() over(partition by is_empty order by seat_no) as rn,
	seat_no - row_number() over(partition by is_empty order by seat_no) as empty_seat_group
	from bms where is_empty = 'Y'),
consecutive_empty_seat as(
	select empty_seat_group, count(1) from empty_seats
	 group by empty_seat_group
	 having count(1) >= 3)
select seat_no, is_empty
from empty_seats a inner join consecutive_empty_seat b
on a.empty_seat_group = b.empty_seat_group


--SQL solution 2 using row_number different level of lag
with previous_and_next_seat as (
	select *,
	lag(is_empty) over(order by seat_no) pre_1,
	lag(is_empty, 2) over(order by seat_no) pre_2,
	lead(is_empty) over(order by seat_no) next_1,
	lead(is_empty, 2) over(order by seat_no) next_2
	from bms)
select seat_no, is_empty
from previous_and_next_seat
where (is_empty = 'Y' and next_1 = 'Y' and next_2 = 'Y')
	or (is_empty = 'Y' and next_1 = 'Y' and pre_1 = 'Y')
	or (is_empty = 'Y' and pre_1 = 'Y' and pre_2 = 'Y')


--SQL solution 3 using advance aggregation
with seat_grouping_count as (
	select *,
	sum(case when is_empty = 'Y' then 1 else 0 end) over(order by seat_no rows between 2 preceding and current row) as prev_2,
	sum(case when is_empty = 'Y' then 1 else 0 end) over(order by seat_no rows between 1 preceding and 1 following) as prev_next_1,
	sum(case when is_empty = 'Y' then 1 else 0 end) over(order by seat_no rows between current row and 2 following) as next_2
	from bms)
select seat_no, is_empty
	from seat_grouping_count
	where is_empty = 'Y' and (prev_2 = 3 or prev_next_1 = 3 or next_2 = 3)
