-- question statement
    -- Get the call numbers having both incoming and outgoing call
    -- Total Out duration should be more than incoming call

-- create table statement
create table call_details  (call_type varchar(10), call_number varchar(12), call_duration int);

-- Insert data
insert into call_details values
('OUT','181868',13),('OUT','2159010',8)
,('OUT','2159010',178),('SMS','4153810',1),('OUT','2159010',152),('OUT','9140152',18),('SMS','4162672',1)
,('SMS','9168204',1),('OUT','9168204',576),('INC','2159010',5),('INC','2159010',4),('SMS','2159010',1)
,('SMS','4535614',1),('OUT','181868',20),('INC','181868',54),('INC','218748',20),('INC','2159010',9)
,('INC','197432',66),('SMS','2159010',1),('SMS','4535614',1);

-- Input data
"call_type","call_number","call_duration"
OUT,"181868",13
OUT,"2159010",8
OUT,"2159010",178
SMS,"4153810",1
OUT,"2159010",152
OUT,"9140152",18
SMS,"4162672",1
SMS,"9168204",1
OUT,"9168204",576
INC,"2159010",5
INC,"2159010",4
SMS,"2159010",1
SMS,"4535614",1
OUT,"181868",20
INC,"181868",54
INC,"218748",20
INC,"2159010",9
INC,"197432",66
SMS,"2159010",1
SMS,"4535614",1

-- Required Output
"call_number"
"2159010"

--Solution steps
-- 1. filter out SMS records
-- 2. group by call number get the sum of duration with case conditions
-- 3. one condition to get only some of out going call or the number other to sum of incoming
-- 4. save the info in temp  table and filter the records having more outgoing duration than in coming

--SQL solution1 using CTE and sum()
with cte as (
select
call_number,
sum(case when call_type = 'OUT' then call_duration else null end) as out_duration,
sum(case when call_type = 'INC' then call_duration else null end) as in_duration
from call_details
where call_type != 'SMS'
group by call_number)
select call_number
from cte where out_duration > in_duration


--SQL solution2 using having
select
call_number
from call_details
where call_type != 'SMS'
group by call_number
having sum(case when call_type = 'OUT' then call_duration else null end) > sum(case when call_type = 'INC' then call_duration else null end)

--SQL solution3 using self join
with cte as (
	select
	call_number, call_type,
	sum(call_duration) as call_duration
	from call_details
	where call_type != 'SMS'
	group by call_number, call_type)
select
a.call_number
from cte a inner join cte b on
a.call_number = b.call_number and
a.call_type > b.call_type and
a.call_duration > b.call_duration