-- question statement
    -- Deduplicate city_distance so that A->B and B->A pairs with the
    -- SAME distance are treated as duplicates -- keep only the first
    -- one. If A->B and B->A have DIFFERENT distances, keep both rows
    -- (they're not true duplicates).


-- create table statement
CREATE TABLE city_distance (
    distance     INT,
    source       VARCHAR(512),
    destination  VARCHAR(512)
);


-- insert data
INSERT INTO city_distance(distance, source, destination) VALUES (100, 'New Delhi', 'Panipat');
INSERT INTO city_distance(distance, source, destination) VALUES (200, 'Ambala', 'New Delhi');
INSERT INTO city_distance(distance, source, destination) VALUES (150, 'Bangalore', 'Mysore');
INSERT INTO city_distance(distance, source, destination) VALUES (150, 'Mysore', 'Bangalore');
INSERT INTO city_distance(distance, source, destination) VALUES (250, 'Mumbai', 'Pune');
INSERT INTO city_distance(distance, source, destination) VALUES (250, 'Pune', 'Mumbai');
INSERT INTO city_distance(distance, source, destination) VALUES (2500, 'Chennai', 'Bhopal');
INSERT INTO city_distance(distance, source, destination) VALUES (2500, 'Bhopal', 'Chennai');
INSERT INTO city_distance(distance, source, destination) VALUES (60, 'Tirupati', 'Tirumala');
INSERT INTO city_distance(distance, source, destination) VALUES (80, 'Tirumala', 'Tirupati');


-- required output (7 rows: 2 unpaired + 3 deduped pairs kept once + 2 kept because distance differs)
"distance","source","destination"
100,New Delhi,Panipat
200,Ambala,New Delhi
150,Bangalore,Mysore          <-- "first" of the Bangalore/Mysore pair (as originally inserted)
250,Mumbai,Pune               <-- "first" of the Mumbai/Pune pair
2500,Chennai,Bhopal           <-- "first" of the Chennai/Bhopal pair
60,Tirupati,Tirumala          <-- kept: distances differ (60 vs 80), not a true duplicate
80,Tirumala,Tirupati          <-- kept: same reason


-- solution steps

-- Step 1:
-- For each row, self-join to find its "mirror" row: same distance,
-- with source/destination swapped. If no mirror exists (Delhi/
-- Panipat, Ambala/Delhi), the row is unique by definition -- keep it.

-- Step 2:
-- If a mirror DOES exist, exactly one of the pair must be kept.
-- This is the step where your three attempts differ.


-- attempt 1 (self-join + alphabetical tie-break -- verified runs, but see notes)
select a.*
from city_distance a
left join city_distance b
    on a.distance = b.distance
   and a.source = b.destination
   and a.destination = b.source
where (b.distance is null)
   or (b.distance is not null and a.source < a.destination);


-- attempt 2 (normalize pair + row_number -- verified runs, closer to "keep first")
with cte as (
    select *,
        case when source < destination then source else destination end as city1,
        case when source > destination then source else destination end as city2,
        row_number() over (order by (select null)) as rn
    from city_distance
),
city_distance_details as (
    select *,
        row_number() over (partition by distance, city1, city2 order by rn) as rn2
    from cte
)
select distance, source, destination
from city_distance_details
where rn2 = 1;


