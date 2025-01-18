-- question statement
    -- Identify 4 consecutive empty rows in a row

-- create table statement
create table movie(seat varchar(50),occupancy int);

-- Insert data
insert into movie values
('a1',1),('a2',1),('a3',0),('a4',0),('a5',0),
('a6',0),('a7',1),('a8',1),('a9',0),('a10',0),
('b1',0),('b2',0),('b3',0),('b4',1),('b5',1),
('b6',1),('b7',1),('b8',0),('b9',0),('b10',0),
('c1',0),('c2',1),('c3',0),('c4',1),('c5',1),
('c6',0),('c7',1),('c8',0),('c9',0),('c10',1);

-- Input data
"seat","occupancy"
a1,1
a2,1
a3,0
a4,0
a5,0
a6,0
a7,1
a8,1
a9,0
a10,0
b1,0
b2,0
b3,0
b4,1
b5,1
b6,1
b7,1
b8,0
b9,0
b10,0
c1,0
c2,1
c3,0
c4,1
c5,1
c6,0
c7,1
c8,0
c9,0
c10,1

-- Required Output
"seat","occupancy"
a3,0
a4,0
a5,0
a6,0

--Solution steps
-- 1. get the seat number and row separated from the seat column
-- 2. Filter the empty seats
-- 3. Calculate seat number - row_number partition by row and order by seat number
-- 4. this calculation will create a group
-- 5. Get a running count or seat partition by seat_row and new column row_number
-- 6. Save the data in temp table and apply the filter on count column to get 4 or more empty seats.

--SQL solution1 using Row number
with cte as (
	select
		seat,
		occupancy,
		left(seat, 1) seat_row,
		cast(substring(seat, 2, 2) as integer) - row_number() over(partition by left(seat, 1) order by cast(substring(seat, 2, 2) as integer)) as rn
	from movie
	where occupancy = 0),
empty_seat_count as(
	select
		*,
		count(seat) over(partition by seat_row, rn) seat_count
	from cte)
select
seat,
occupancy
from empty_seat_count
where seat_count > 3

--SQL solution1 using max and count
with cte as(
	select
	*,
	left(seat, 1) as seat_row,
	cast(substring(seat, 2, 2) as integer) as seat_no
	from movie)
select
	*,
	max(occupancy) over(partition by seat_row order by seat_no rows between current row and 3 following) as is_empty,
	count(occupancy) over(partition by seat_row order by seat_no rows between current row and 3 following) as cnt
from cte