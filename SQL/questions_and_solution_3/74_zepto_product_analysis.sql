-- question statement
    -- For each number n in a table, generate n as a repeated
    -- sequence n times. E.g. input 1,2,3 -> output:
    --     1
    --     2, 2
    --     3, 3, 3

-- create table statement
create table numbers (n int);


-- Insert data
insert into numbers values (1),(2),(3),(4),(5);
insert into numbers values (9);


-- Input data
"n"
1
2
3
4
5
9


-- Required Output (verified: executed against sqlite3)
"n"
1
2
2
3
3
3
4
4
4
4
5
5
5
5
5
9
9
9
9
9
9
9
9
9

-- 24 total rows: 1(x1) + 2(x2) + 3(x3) + 4(x4) + 5(x5) + 9(x9) = 24


--Solution steps
-- 1. For each number n, start a counter n1 at 1 (base case of the
--    recursion) -- one row per number to begin with.
-- 2. Recursively increment n1 by 1, but only while n1+1 is still
--    <= n -- this generates exactly n rows total for that number
--    (n1 = 1, 2, 3, ..., n), then stops.
-- 3. Since every number's expansion runs independently and in
--    parallel within the same recursive CTE, larger numbers (like 9)
--    simply keep recursing for more iterations than smaller ones
--    (like 1, which never recurses past the base case at all).
-- 4. The final SELECT only needs n -- n1 was purely scaffolding to
--    control how many times each n gets duplicated, and is dropped
--    once its job is done.


--SQL solution
with recursive cte as (
	select n, 1 as n1 from numbers
	union all
	select n, n1+1 from cte
	where n1+1 <= n
)
select n from cte
order by n;