-- question statement
    -- For each job position, list every post (filled and vacant) up to
    -- totalpost. Filled posts show the employee name; unfilled posts
    -- show 'Vacant'. Output columns: title, groups, levels, payscale,
    -- emp_name.


-- create table statement
create table job_positions (
    id         int,
    title      varchar(100),
    groups     varchar(10),
    levels     varchar(10),
    payscale   int,
    totalpost  int
);

create table job_employees (
    id           int,
    name         varchar(100),
    position_id  int
);


-- insert data
insert into job_positions values (1, 'General manager', 'A', 'l-15', 10000, 1);
insert into job_positions values (2, 'Manager', 'B', 'l-14', 9000, 5);
insert into job_positions values (3, 'Asst. Manager', 'C', 'l-13', 8000, 10);

insert into job_employees values (1, 'John Smith', 1);
insert into job_employees values (2, 'Jane Doe', 2);
insert into job_employees values (3, 'Michael Brown', 2);
insert into job_employees values (4, 'Emily Johnson', 2);
insert into job_employees values (5, 'William Lee', 3);
insert into job_employees values (6, 'Jessica Clark', 3);
insert into job_employees values (7, 'Christopher Harris', 3);
insert into job_employees values (8, 'Olivia Wilson', 3);
insert into job_employees values (9, 'Daniel Martinez', 3);
insert into job_employees values (10, 'Sophia Miller', 3);


-- input data
"id","title","groups","levels","payscale","totalpost"
1,General manager,A,l-15,10000,1
2,Manager,B,l-14,9000,5
3,Asst. Manager,C,l-13,8000,10

"id","name","position_id"
1,John Smith,1
2,Jane Doe,2
3,Michael Brown,2
4,Emily Johnson,2
5,William Lee,3
6,Jessica Clark,3
7,Christopher Harris,3
8,Olivia Wilson,3
9,Daniel Martinez,3
10,Sophia Miller,3


-- required output (verified: executed against sqlite3, all 16 rows match)
"title","groups","levels","payscale","emp_name"
General manager,A,l-15,10000,John Smith
Manager,B,l-14,9000,Jane Doe
Manager,B,l-14,9000,Michael Brown
Manager,B,l-14,9000,Emily Johnson
Manager,B,l-14,9000,Vacant
Manager,B,l-14,9000,Vacant
Asst. Manager,C,l-13,8000,William Lee
Asst. Manager,C,l-13,8000,Jessica Clark
Asst. Manager,C,l-13,8000,Christopher Harris
Asst. Manager,C,l-13,8000,Olivia Wilson
Asst. Manager,C,l-13,8000,Daniel Martinez
Asst. Manager,C,l-13,8000,Sophia Miller
Asst. Manager,C,l-13,8000,Vacant
Asst. Manager,C,l-13,8000,Vacant
Asst. Manager,C,l-13,8000,Vacant
Asst. Manager,C,l-13,8000,Vacant


-- solution steps

-- Step 1:
-- Recursively expand each position row into `totalpost` numbered
-- "slots" (rn = 1 .. totalpost). This is what turns "1 position row
-- with totalpost=5" into 5 individual rows to fill/leave vacant.

-- Step 2:
-- Number the employees within each position_id (row_number ordered
-- by employee id), so each employee gets a slot number (rn) matching
-- the order they'd fill posts in.

-- Step 3:
-- Left join the expanded slots (cte) to the numbered employees on
-- both position_id and matching slot number (rn = rn). Slots with
-- no matching employee rn naturally produce NULL name.

-- Step 4:
-- coalesce the NULLs to 'Vacant' for unfilled posts.


-- sql solution
with recursive cte as (
    select
        id, title, groups, levels, payscale, totalpost,
        1 as rn
    from job_positions

    union all

    select
        id, title, groups, levels, payscale, totalpost,
        rn + 1 as rn
    from cte
    where rn < totalpost
),
positions as (
    select
        *,
        row_number() over (partition by position_id order by id) as rn
    from job_employees
)
select
    a.title,
    a.groups,
    a.levels,
    a.payscale,
    coalesce(b.name, 'Vacant') as emp_name
from cte as a
left join positions b
    on a.id = b.position_id
   and a.rn = b.rn
order by a.id, a.rn;


-- approach 2
with recursive tally(n) as (
    select 1
    union all
    select n + 1 from tally where n < (select max(totalpost) from job_positions)
),
slots as (
    select p.id, p.title, p.groups, p.levels, p.payscale, t.n as rn
    from job_positions p
    join tally t on t.n <= p.totalpost
),
positions as (
    select *, row_number() over (partition by position_id order by id) as rn
    from job_employees
)
select
    slots.title, slots.groups, slots.levels, slots.payscale,
    coalesce(e.name, 'Vacant') as emp_name
from slots
left join positions e
    on slots.id = e.position_id
   and slots.rn = e.rn
order by slots.id, slots.rn;