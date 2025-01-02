-- question statement
    -- Find cities where covid cases are increasing daily

-- create table statement
create table covid(city varchar(50),days date,cases int);

-- Insert data
insert into covid values
	('DELHI','2022-01-01',100),
	('DELHI','2022-01-02',200),
	('DELHI','2022-01-03',300),
	('MUMBAI','2022-01-01',100),
	('MUMBAI','2022-01-02',100),
	('MUMBAI','2022-01-03',300),
	('CHENNAI','2022-01-01',100),
	('CHENNAI','2022-01-02',200),
	('CHENNAI','2022-01-03',150),
	('BANGALORE','2022-01-01',100),
	('BANGALORE','2022-01-02',300),
	('BANGALORE','2022-01-03',200),
	('BANGALORE','2022-01-04',400);

-- Input data
"city","days","cases"
DELHI,2022-01-01,100
DELHI,2022-01-02,200
DELHI,2022-01-03,300
MUMBAI,2022-01-01,100
MUMBAI,2022-01-02,100
MUMBAI,2022-01-03,300
CHENNAI,2022-01-01,100
CHENNAI,2022-01-02,200
CHENNAI,2022-01-03,150
BANGALORE,2022-01-01,100
BANGALORE,2022-01-02,300
BANGALORE,2022-01-03,200
BANGALORE,2022-01-04,400

-- Required Output
"city"
DELHI

--Solution steps
    -- get the previous day cases
    -- substrata previous day cases with the current day cases
    -- get the cities where this difference is going negative for any days
    -- run query to get city not in above list

--SQL solution 1 using lag and not in
with case_history as (
    select *,
        cases - lag(cases) over(partition by city order by days) as increase_in_cases
    from covid c)
select
	distinct city
from case_history
where city not in
	(select city from case_history where increase_in_cases <=0)


--SQL solution 2 using rank and distinct count in having
with ranking_diff as (
	select
		*,
		rank() over(partition by city order by days) - rank() over(partition by city order by cases) as rank_dif
	from covid)
select city
from ranking_diff
group by city
having count(distinct rank_dif) = 1 and max(rank_dif) = 0
