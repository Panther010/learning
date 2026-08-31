-- question statement
    -- Find all seat_ids that are part of a group of 2 or more
    -- CONSECUTIVE free seats (free = 1). Isolated free seats (no
    -- free neighbor on either side) should be excluded.

-- create table statement
CREATE TABLE cinema (
    seat_id INT PRIMARY KEY,
    free    int
);


-- Insert data
INSERT INTO cinema (seat_id, free) VALUES (1, 1);
INSERT INTO cinema (seat_id, free) VALUES (2, 0);
INSERT INTO cinema (seat_id, free) VALUES (3, 1);
INSERT INTO cinema (seat_id, free) VALUES (4, 1);
INSERT INTO cinema (seat_id, free) VALUES (5, 1);
INSERT INTO cinema (seat_id, free) VALUES (6, 0);
INSERT INTO cinema (seat_id, free) VALUES (7, 1);
INSERT INTO cinema (seat_id, free) VALUES (8, 1);
INSERT INTO cinema (seat_id, free) VALUES (9, 0);
INSERT INTO cinema (seat_id, free) VALUES (10, 1);
INSERT INTO cinema (seat_id, free) VALUES (11, 0);
INSERT INTO cinema (seat_id, free) VALUES (12, 1);
INSERT INTO cinema (seat_id, free) VALUES (13, 0);
INSERT INTO cinema (seat_id, free) VALUES (14, 1);
INSERT INTO cinema (seat_id, free) VALUES (15, 1);
INSERT INTO cinema (seat_id, free) VALUES (16, 0);
INSERT INTO cinema (seat_id, free) VALUES (17, 1);
INSERT INTO cinema (seat_id, free) VALUES (18, 1);
INSERT INTO cinema (seat_id, free) VALUES (19, 1);
INSERT INTO cinema (seat_id, free) VALUES (20, 1);


-- Input data
"seat_id","free"
1,1
2,0
3,1
4,1
5,1
6,0
7,1
8,1
9,0
10,1
11,0
12,1
13,0
14,1
15,1
16,0
17,1
18,1
19,1
20,1


-- Required Output (verified: all 3 solutions below produce this
-- identically, executed against sqlite3)
"seat_id"
3
4
5
7
8
14
15
17
18
19
20

-- runs, for reference:
-- seat 1: isolated (neighbor 2 is taken) -- excluded
-- seats 3,4,5: run of 3 -- included
-- seats 7,8: run of 2 -- included
-- seat 10: isolated (9 and 11 both taken) -- excluded
-- seat 12: isolated (11 and 13 both taken) -- excluded
-- seats 14,15: run of 2 -- included
-- seats 17,18,19,20: run of 4 -- included


--Solution steps

--SQL solution1 -- gaps-and-islands (seat_id - row_number trick)
-- Filtering to free seats only, then taking (seat_id - row_number())
-- ordered by seat_id: for any run of truly consecutive seat_ids,
-- this difference stays CONSTANT (both seat_id and row_number
-- increase by exactly 1 each step), so every seat in one run shares
-- the same "grp" value -- classic gaps-and-islands. Counting rows
-- per grp and keeping groups with count > 1 gives runs of 2+.

with cte as (
select
    *,
    row_number() over(order by seat_id) as rn,
    seat_id - row_number() over(order by seat_id) as grp
from cinema
where free = 1
order by free, seat_id
),
grp as(
select
    *,
    count(*) over(partition by grp) as grp_count
from cte)
select seat_id from grp where grp_count > 1
order by seat_id;


--SQL solution2 -- self-join on adjacent seat_id
-- Directly join the table to itself on "this seat's neighbor is one
-- seat_id lower," keeping only pairs where BOTH are free. Each match
-- proves both seat_ids in the pair belong to a run of 2+. Union the
-- two sides together (dedupes automatically) to get every seat that
-- has at least one free neighbor.

with cte as (
select
	c1.seat_id as s1, c2.seat_id as s2
from cinema c1 join cinema c2 on c1.seat_id = c2.seat_id + 1
where c1.free = 1 and c2.free = 1
)
select s1 as seat_id from cte
union
select s2 as seat_id from cte
order by seat_id;


--SQL solution3 -- lead/lag neighbor check
-- For each free seat, look directly at its immediate left (lag) and
-- right (lead) neighbor's free status. If either neighbor is also
-- free, this seat is part of a run of 2+.

with cte as (
select
    *,
    lead(free) over(order by seat_id) next_seat,
    lag(free) over(order by seat_id) prev_seat
from cinema)
select seat_id from cte
where free = 1 and (next_seat = 1 or prev_seat = 1)
order by seat_id;
