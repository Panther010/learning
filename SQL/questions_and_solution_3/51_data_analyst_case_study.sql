-- question statement
    --we have data of bookings and another table for segment
    -- solve following question
    -- 1. calculate total user count for each segment and for each segment user who booked flight in apr 2022
    -- 2. write a query to get the users whose first booking was a hotel booking
    -- 3. write a query to find days between first and last booking of each days
    -- 4. write a query to find number of hotel bookings for each of the user segment for the year 2022

-- create table statement update
--Booking_table
CREATE TABLE booking_table(
   booking_id       VARCHAR(3) NOT NULL
  ,booking_date     date NOT NULL
  ,user_id          VARCHAR(2) NOT NULL
  ,line_of_business VARCHAR(6) NOT NULL
);
-- user_table
CREATE TABLE user_table(
   user_id VARCHAR(3) NOT NULL
  ,segment VARCHAR(2) NOT NULL
);

-- Insert data
--Booking_table
INSERT INTO booking_table values
('b1','2022-03-23','u1','Flight'),
('b2','2022-03-27','u2','Flight'),
('b3','2022-03-28','u1','Hotel'),
('b4','2022-03-31','u4','Flight'),
('b5','2022-04-02','u1','Hotel'),
('b6','2022-04-02','u2','Flight'),
('b7','2022-04-06','u5','Flight'),
('b8','2022-04-06','u6','Hotel'),
('b9','2022-04-06','u2','Flight'),
('b10','2022-04-10','u1','Flight'),
('b11','2022-04-12','u4','Flight'),
('b12','2022-04-16','u1','Flight'),
('b13','2022-04-19','u2','Flight'),
('b14','2022-04-20','u5','Hotel'),
('b15','2022-04-22','u6','Flight'),
('b16','2022-04-26','u4','Hotel'),
('b17','2022-04-28','u2','Hotel'),
('b18','2022-04-30','u1','Hotel'),
('b19','2022-05-04','u4','Hotel'),
('b20','2022-05-06','u1','Flight');

-- user_table
INSERT INTO user_table values('u1','s1'), ('u2','s1'), ('u3','s1'), ('u4','s2'), ('u5','s2'), ('u6','s3'), ('u7','s3'), ('u8','s3'), ('u9','s3'), ('u10','s3');

-- Input data
--Booking_table
"booking_id","booking_date","user_id","line_of_business"
b1,2022-03-23,u1,Flight
b2,2022-03-27,u2,Flight
b3,2022-03-28,u1,Hotel
b4,2022-03-31,u4,Flight
b5,2022-04-02,u1,Hotel
b6,2022-04-02,u2,Flight
b7,2022-04-06,u5,Flight
b8,2022-04-06,u6,Hotel
b9,2022-04-06,u2,Flight
b10,2022-04-10,u1,Flight
b11,2022-04-12,u4,Flight
b12,2022-04-16,u1,Flight
b13,2022-04-19,u2,Flight
b14,2022-04-20,u5,Hotel
b15,2022-04-22,u6,Flight
b16,2022-04-26,u4,Hotel
b17,2022-04-28,u2,Hotel
b18,2022-04-30,u1,Hotel
b19,2022-05-04,u4,Hotel
b20,2022-05-06,u1,Flight

-- user_table
"user_id","segment"
u1,s1
u2,s1
u3,s1
u4,s2
u5,s2
u6,s3
u7,s3
u8,s3
u9,s3
u10,s3


-- Required Output
--Q1
"segment","total_user_count","user_who_booked_flight_in_apr2022"
s1,3,2
s2,2,2
s3,5,1


--Solution steps
-- 1. left join user_table and booking table on user_id
--2. count distinct user_id
--3. with in case class apply condition to fetch user_id from apr 2022

--SQL solution1
with booking_and_segment as (
	select
		distinct b.user_id, segment
	from booking_table a inner join user_table b
	on a.user_id = b.user_id and a.line_of_business = 'Flight' and date_part('month', booking_date) = 4
),
apr_flight_booking_segment as (
	select
		segment,
		count(user_id) as user_who_booked_flight_in_apr2022
	from booking_and_segment
	group by segment
),
segment_user_count as(
	select
		segment,
		count(user_id) as total_user_count
	from user_table
	group by segment
)
select
	a1.segment,
	a1.total_user_count,
	b1.user_who_booked_flight_in_apr2022
from segment_user_count a1 left join apr_flight_booking_segment b1
	on a1.segment = b1.segment
order by a1.segment

--SQL solution2

select
	segment,
	count(distinct a.user_id) as total_user_count,
	count(distinct
		case when line_of_business = 'Flight' and
		booking_date between '2022-04-01' and '2022-04-30'
	then a.user_id end) as user_who_booked_flight_in_apr2022
from user_table a left join booking_table b on a.user_id = b.user_id
group by segment;

select
	segment,
	count(distinct a.user_id) as total_user_count,
	count(distinct
		case when line_of_business = 'Flight' and
		date_part('month', booking_date) = 4 and
		date_part('year', booking_date) = 2022
	then a.user_id end) as user_who_booked_flight_in_apr2022
from user_table a left join booking_table b on a.user_id = b.user_id
group by segment

--Q1
"booking_id","booking_date","user_id","line_of_business","rn"
b8,2022-04-06,u6,Hotel,1


--Solution steps
--1. rank by user order by booking_date

--SQL solution1
with user_booking_rank as (
	select
		*,
		rank() over(partition by user_id order by booking_date) as rn
	from booking_table
)
select * from user_booking_rank
where rn = 1 and line_of_business = 'Hotel'

--SQL solution2
with user_booking_rank as (
	select
		*,
		first_value(line_of_business) over(partition by user_id order by booking_date) as rn
	from booking_table
)

select * from user_booking_rank
where rn = 'Hotel' and line_of_business = 'Hotel'


--Q3
"user_id","days_between"
u4,34
u5,14
u1,44
u2,32
u6,16

--Solution steps
--1. get max date and min date and calculate the difference

--SQL solution1
select
	user_id,
	(max(booking_date) - min(booking_date)) as days_between
from booking_table
group by user_id

--SQL solution2
select distinct
	user_id,
	first_value(booking_date) over(partition by user_id order by booking_date),
	last_value(booking_date) over(partition by user_id),
	last_value(booking_date) over(partition by user_id) -
	first_value(booking_date) over(partition by user_id order by booking_date) as days_between
from booking_table
order by user_id

--Q4
"segment","flight_bookings","hotel_bookings"
s1,8,4
s2,3,3
s3,1,1

--Solution steps
--1. case condition with in some

--SQL solution1
select
	segment,
	sum(case when line_of_business = 'Flight' then 1 else 0 end) as flight_bookings,
	sum(case when line_of_business = 'Hotel' then 1 else 0 end) as hotel_bookings
from user_table a left join booking_table b on
	a.user_id = b.user_id
group by segment
order by segment

--SQL solution2
select
	segment,
	line_of_business,
	count(a.user_id) as booking_count
from user_table a inner join booking_table b on
	a.user_id = b.user_id and
	date_part('year', booking_date) = '2022'
group by segment, line_of_business
order by segment