-- question statement
    --We have a table which stores multiple sections, every section has 3 numbers. We have to find 4 numbers from any 2 sections
    --(2 numbers each) whose addition should be max
    --In case there us same total for 2 sections section with high individual number will get preference.
    --current scenario out of C and D D will get preference since D is having one number with 10

-- create table statement update
create table section_data
(
section varchar(5),
number integer
);

-- Insert data
insert into section_data
values ('A',5),('A',7),('A',10) ,('B',7),('B',9),('B',10) ,('C',9),('C',7),('C',9) ,('D',10),('D',3),('D',8);

-- Input data
"section","number"
A,5
A,7
A,10
B,7
B,9
B,10
C,9
C,7
C,9
D,10
D,3
D,8

-- Required Output
"section","number"
B,10
B,9
D,10
D,8

--Solution steps
-- 1. Calculate row_number for each section having number as desc to select the highest 2 marks for each section
-- 2. apply filter section_number_rank < 3 to remove other data.
-- 3. Calculate the total for each section and the max marks from each section
-- 4. apply dense rank on the section total marks and max marks to get highest total with high mark ranking
-- 5. apply fiter to remove unfiltered data

--SQL solution1

with ranked_section as (
	select
		*,
		row_number() over(partition by section order by number desc) as section_number_rank
	from section_data
),
section_total as (
	select
		*,
		sum(number) over(partition by section) as section_marks,
		max(number) over(partition by section) as mn
	from ranked_section where section_number_rank < 3),
section_total_ranking as (
	select
		*, dense_rank() over(order by section_marks desc, mn desc) as sm
	from section_total
)
select section, number from section_total_ranking where sm < 3

