-- question statement
    -- For each experience level, count the total number of
    -- candidates and how many of them got a perfect score in every
    -- category they were asked to complete. A NULL score means the
    -- candidate was not asked to solve that category's task, and
    -- should be treated as a perfect score (100) for that category
    -- when checking whether they got a perfect overall result.
    -- 100 is a perfect score in a single category.

-- create table statement
create table assessments (
    id           int,
    experience   int,
    sql          int,
    algo         int,
    bug_fixing   int
);


-- Insert data (two example datasets -- the script deletes and
-- re-inserts, so only dataset 2 is actually left in the table if run
-- top to bottom as written; both are shown here as separate test cases)

-- dataset 1
insert into assessments values
(1,3,100,null,50),
(2,5,null,100,100),
(3,1,100,100,100),
(4,5,100,50,null),
(5,5,100,100,100);

-- dataset 2
insert into assessments values
(1,2,null,null,null),
(2,20,null,null,20),
(3,7,100,null,100),
(4,3,100,50,null),
(5,2,40,100,100);


-- Input data (dataset 2 -- the one actually left in the table)
"id","experience","sql","algo","bug_fixing"
1,2,,,
2,20,,,20
3,7,100,,100
4,3,100,50,
5,2,40,100,100


-- Required Output (verified: executed against sqlite3 -- both
-- solutions below produce identical results on both datasets)

-- dataset 1:
"experience","total_student","max_score_students"
1,1,1
3,1,0
5,3,2

-- dataset 2:
"experience","total_student","max_score_students"
2,2,1
3,1,0
7,1,1
20,1,0

-- reasoning, dataset 2:
-- id1 (exp=2): all 3 categories NULL -> treated as 100+100+100=300
--   -> PERFECT (never asked to solve anything, so "perfect by
--   default")
-- id2 (exp=20): sql=null(100), algo=null(100), bug=20 -> 220 -> not perfect
-- id3 (exp=7): sql=100, algo=null(100), bug=100 -> 300 -> PERFECT
-- id4 (exp=3): sql=100, algo=50, bug=null(100) -> 250 -> not perfect
-- id5 (exp=2): sql=40, algo=100, bug=100 -> 240 -> not perfect
-- exp=2 group: 2 candidates (id1, id5), 1 perfect (id1)


--Solution steps
-- 1. For each candidate, treat a NULL category score as 100 (using
--    coalesce) -- this is the key rule from the question: not being
--    asked to do a task counts as a perfect result for that task,
--    not as a missing/zero score.
-- 2. Sum the three (coalesced) category scores. Since each category
--    maxes out at 100, a candidate who's perfect across everything
--    they were actually asked to do (and untouched-by-default on
--    anything they weren't) will always total exactly 300.
-- 3. Group by experience, count total candidates, and count how many
--    hit that 300 total.


--SQL solution1 -- via a CTE (computes total_score once, reused)
with total_score_details as (
	select
		*,
		coalesce(sql, 100) + coalesce(algo, 100) + coalesce(bug_fixing, 100) as total_score
	from assessments)
select
	experience,
	count(id) as total_student,
	sum(case when total_score = 300 then 1 else 0 end) as max_score_students
from total_score_details
group by experience
order by experience;


--SQL solution2 -- inline (same logic, computed directly in the CASE)
select
	experience,
	count(id) as total_student,
	sum(case when (coalesce(sql, 100) + coalesce(algo, 100) + coalesce(bug_fixing, 100)) = 300 then 1 else 0 end) max_score_students
from assessments
group by experience
order by experience;


