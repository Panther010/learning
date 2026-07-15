-- question statement
    -- Split a full customer_name into first_name, middle_name, and
    -- last_name, handling names with 1, 2, or 3 space-separated parts.


-- create table statement
create table customers (
    customer_name varchar(30)
);


-- insert data
insert into customers values
('Ankit Bansal'),
('Vishal Pratap Singh'),
('Michael');


-- input data
"customer_name"
Ankit Bansal
Vishal Pratap Singh
Michael


-- required output (verified: executed with split_part semantics reproduced in Python/sqlite)
"customer_name","first_name","middle_name","last_name"
Ankit Bansal,Ankit,,Bansal
Vishal Pratap Singh,Vishal,Pratap,Singh
Michael,Michael,,


-- solution steps

-- Step 1:
-- first_name is always split_part(name, ' ', 1) -- the first token,
-- regardless of how many parts the name has.

-- Step 2:
-- Use split_part(name, ' ', 3) as a probe to detect whether the name
-- has 3 parts. Postgres split_part returns '' (not NULL) when the
-- requested part doesn't exist, which is what makes the != '' check
-- work as a "does a 3rd word exist" test.

-- Step 3:
-- middle_name only exists when there IS a 3rd part -- in that case
-- it's the 2nd token. Otherwise it's blank (2-part and 1-part names
-- have no middle name).

-- Step 4:
-- last_name is the 3rd token if it exists; otherwise fall back to
-- the 2nd token (2-part name case); otherwise blank (1-part name,
-- e.g. 'Michael', has no last name at all).


-- sql solution
select
    customer_name,
    split_part(customer_name, ' ', 1) as first_name,
    case
        when split_part(customer_name, ' ', 3) != '' then split_part(customer_name, ' ', 2)
        else ''
    end as middle_name,
    case
        when split_part(customer_name, ' ', 3) != '' then split_part(customer_name, ' ', 3)
        when split_part(customer_name, ' ', 2) != '' then split_part(customer_name, ' ', 2)
        else ''
    end as last_name
from customers;

-- Alternative approach worth knowing (regexp_split_to_array):
select
    customer_name,
    (regexp_split_to_array(customer_name, '\s+'))[1] as first_name,
    case when array_length(regexp_split_to_array(customer_name, '\s+'), 1) = 3
         then (regexp_split_to_array(customer_name, '\s+'))[2]
         else '' end as middle_name,
    case when array_length(regexp_split_to_array(customer_name, '\s+'), 1) >= 2
         then (regexp_split_to_array(customer_name, '\s+'))[
              array_length(regexp_split_to_array(customer_name, '\s+'), 1)]
         else '' end as last_name
from customers;
-- This version uses "always take the LAST array element as
-- last_name" instead of hardcoding position 3, so it degrades more
-- gracefully for 4+ word names (last_name is always correct; only
-- middle_name's "just the 2nd word" definition would still need a
-- decision for names with 2+ middle words).