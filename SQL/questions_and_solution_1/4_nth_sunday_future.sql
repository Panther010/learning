-- question statement
--Write a query to provide the date for nth Occurrence in future for given date

-- create table statement

-- Insert data

-- Input data

-- Required Output
--Write a query to provide the date for nth Occurrence in future for given date

--Solution steps
-- declare variable for current date or given date
-- declare variable for nth occurrence
-- get the week day of given date date_part('dow', my_date)
-- get 7 and add it to the given date and cast it to integer
-- subtract date number from 7 and add it to the given date to get next sunday
-- add 7 * (n-1) to date to get nth sunday

--SQL solution1
    with my_data (my_date, n) as (values (current_date, 1))
    select my_date + cast(7 - date_part('dow', my_date) as integer) + ((n-1) * 7) as nth_sunday
    from my_data;

--Additional logics
    with my_data (date_today, n) as (values(current_date, 7))
    select
    date_today,
    date_today + cast(7 - date_part('dow', date_today) as integer) as next_sunday,
    date_today + cast(7 - date_part('dow', date_today) as integer) + ((n-1) * 7) as nth_sunday,
    n
    from my_data
-- sql solution 3
with my_records (my_date, n) as (values(current_date, 5))
select
	my_date + cast(7 - date_part('dow', my_date) as integer) as next_sunday,
	my_date + cast(7 - date_part('dow', my_date) as integer) + (7 * (n -1)) as nth_sunday
from my_records