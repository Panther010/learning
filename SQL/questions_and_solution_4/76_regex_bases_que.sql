-- question statement
    -- Find phone numbers that have no repeating digits, ignoring the
    -- country code prefix when checking for duplicates.

-- create table statement
create table phone_numbers (num varchar(20));


-- Insert data
insert into phone_numbers values
('1234567780'),
('2234578996'),
('+1-12244567780'),
('+32-2233567889'),
('+2-23456987312'),
('+91-9087654123'),
('+23-9085761324'),
('+11-8091013345');


-- Input data
"num"
1234567780
2234578996
+1-12244567780
+32-2233567889
+2-23456987312
+91-9087654123
+23-9085761324
+11-8091013345


-- Required Output (verified: executed logic against the sample data)
"num"
+91-9087654123
+23-9085761324

-- reasoning, after stripping country code where present:
-- 1234567780      -> 1234567780     -- '7' repeats -> excluded
-- 2234578996      -> 2234578996     -- '2','9' repeat -> excluded
-- +1-12244567780  -> 12244567780    -- '2','4','7' repeat -> excluded
-- +32-2233567889  -> 2233567889     -- '2','3','8' repeat -> excluded
-- +2-23456987312  -> 23456987312    -- '2','3' repeat -> excluded
-- +91-9087654123  -> 9087654123     -- all 10 digits 0-9, each once -> KEPT
-- +23-9085761324  -> 9085761324     -- all 10 digits 0-9, each once -> KEPT
-- +11-8091013345  -> 8091013345     -- '0','1','3' repeat -> excluded


--Solution steps
-- 1. Strip the country code: if the number contains a '-', keep only
--    the part AFTER it (the local number). If there's no '-' at all,
--    the number has no country code to strip, so use it as-is.
-- 2. Explode the remaining (country-code-free) digits into one row
--    per character, using regexp_split_to_table with an empty
--    pattern -- a common Postgres trick for splitting a string into
--    individual characters.
-- 3. Group back by the original number, and compare the total digit
--    count to the DISTINCT digit count. If they're equal, every
--    digit in that number is unique -- no repeats.


--SQL solution
with cte as (
select
	*,
	case when position('-' in num) = 0 then num
	else split_part(num, '-', 2) end as new_num
from phone_numbers),
separate_digit as (
select
	*,
	regexp_split_to_table(new_num, '') as digit
from cte)
select num
from separate_digit
group by num, new_num
having count(digit) = count(distinct digit);
