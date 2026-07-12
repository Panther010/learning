-- question statement
    -- Each customer has a set of one-way travel legs (start_loc -> end_loc)
    -- that together form a single travel chain (not necessarily inserted
    -- in order). Find each customer's overall start city (the city that
    -- is never anyone's destination) and overall end city (the city that
    -- is never anyone's origin).


-- create table statement
CREATE TABLE travel_data (
    customer  VARCHAR(10),
    start_loc VARCHAR(50),
    end_loc   VARCHAR(50)
);


-- insert data
INSERT INTO travel_data (customer, start_loc, end_loc) VALUES
    ('c1', 'New York', 'Lima'),
    ('c1', 'London', 'New York'),
    ('c1', 'Lima', 'Sao Paulo'),
    ('c1', 'Sao Paulo', 'New Delhi'),
    ('c2', 'Mumbai', 'Hyderabad'),
    ('c2', 'Surat', 'Pune'),
    ('c2', 'Hyderabad', 'Surat'),
    ('c3', 'Kochi', 'Kurnool'),
    ('c3', 'Lucknow', 'Agra'),
    ('c3', 'Agra', 'Jaipur'),
    ('c3', 'Jaipur', 'Kochi');


-- input data
"customer","start_loc","end_loc"
c1,New York,Lima
c1,London,New York
c1,Lima,Sao Paulo
c1,Sao Paulo,New Delhi
c2,Mumbai,Hyderabad
c2,Surat,Pune
c2,Hyderabad,Surat
c3,Kochi,Kurnool
c3,Lucknow,Agra
c3,Agra,Jaipur
c3,Jaipur,Kochi


-- required output (verified: all 3 solutions below produce this, executed against sqlite3)
"customer","start_loc","end_loc"
c1,London,New Delhi
c2,Mumbai,Pune
c3,Lucknow,Kurnool

-- chains, for reference:
-- c1: London -> New York -> Lima -> Sao Paulo -> New Delhi
-- c2: Mumbai -> Hyderabad -> Surat -> Pune
-- c3: Lucknow -> Agra -> Jaipur -> Kochi -> Kurnool


-- solution steps (your two versions -- same core idea)

-- Step 1:
-- Stack start_loc and end_loc into a single "location" column per
-- customer (UNION ALL), tagging which side each came from.

-- Step 2:
-- A city that appears exactly once across both columns for a
-- customer must be an endpoint of the chain (every "middle" city
-- appears twice: once as someone's end_loc, once as the next leg's
-- start_loc). Filter down to count = 1.

-- Step 3:
-- Recover whether that single-occurrence city was a start_loc or
-- end_loc, then pivot with max()/case to get one row per customer
-- with both columns filled in.


-- sql solution 1 (yours -- group by + having, verified correct)
with travel_city as (
    select customer, start_loc as location
    from travel_data
    union all
    select customer, end_loc as location
    from travel_data
),
city_count as (
    select customer, location, count(location) as city_count
    from travel_city
    group by customer, location
    having count(location) = 1
),
travel_summary as (
    select
        a.customer,
        case when a.start_loc = b.location then a.start_loc else null end as start_loc,
        case when a.end_loc = b.location then a.end_loc else null end as end_loc
    from travel_data a
    inner join city_count b
        on a.customer = b.customer
       and (a.start_loc = b.location or a.end_loc = b.location)
)
select customer, max(start_loc) as start_loc, max(end_loc) as end_loc
from travel_summary
group by customer;


-- sql solution 2 (yours -- window function count, verified correct)
with travel_city as (
    select customer, start_loc as location, 'start_loc' as col_name
    from travel_data
    union all
    select customer, end_loc as location, 'end_loc' as col_name
    from travel_data
),
city_count as (
    select
        customer,
        location,
        count(location) over (partition by customer, location) as loc_count,
        col_name
    from travel_city
)
select
    customer,
    max(case when col_name = 'start_loc' then location end) as start_loc,
    max(case when col_name = 'end_loc' then location end) as end_loc
from city_count
where loc_count = 1
group by customer;


-- alternative solution (anti-join, no union/pivot needed -- verified correct)
select
    s.customer,
    s.start_loc,
    e.end_loc
from (
    select customer, start_loc
    from travel_data a
    where not exists (
        select 1 from travel_data b
        where b.customer = a.customer and b.end_loc = a.start_loc
    )
) s
join (
    select customer, end_loc
    from travel_data a
    where not exists (
        select 1 from travel_data b
        where b.customer = a.customer and b.start_loc = a.end_loc
    )
) e
    on s.customer = e.customer;
