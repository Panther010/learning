-- question statement
    -- Find total no f messages exchange between each person per day

-- create table statement
CREATE TABLE subscriber (sms_date date, sender varchar(20), receiver varchar(20), sms_no int);

-- Insert data
INSERT INTO subscriber VALUES
	('2020-4-1', 'Avinash', 'Vibhor',10),
	('2020-4-1', 'Vibhor', 'Avinash',20),
	('2020-4-1', 'Avinash', 'Pawan',30),
	('2020-4-1', 'Pawan', 'Avinash',20),
	('2020-4-1', 'Vibhor', 'Pawan',5),
	('2020-4-1', 'Pawan', 'Vibhor',8),
	('2020-4-1', 'Vibhor', 'Deepak',50);

-- Input data
    --subscriber

"sms_date","sender","receiver","sms_no"
2020-04-01,Avinash,Vibhor,10
2020-04-01,Vibhor,Avinash,20
2020-04-01,Avinash,Pawan,30
2020-04-01,Pawan,Avinash,20
2020-04-01,Vibhor,Pawan,5
2020-04-01,Pawan,Vibhor,8
2020-04-01,Vibhor,Deepak,50


-- Required Output
"sms_date","sender","receiver","sms_no"
2020-04-01,Avinash,Vibhor,30
2020-04-01,Avinash,Pawan,50
2020-04-01,Vibhor,Deepak,50
2020-04-01,Pawan,Vibhor,13


--Solution steps
    -- exchange sender and receiver in such a way that send should be alphabetically smaller
    -- save it as temp table
    -- group by date, sender and receiver
    -- calculate the total message now

--SQL solution 1 self join
select distinct
	a.sms_date,
	case when (a.sender < b.sender) or (b.sender is null) then a.sender else b.sender end as sender,
	case when (a.receiver > b.receiver) or (b.receiver is null) then a.receiver else b.receiver end as receiver,
	case when b.sms_no is null then a.sms_no else a.sms_no + b.sms_no end as sms_no
from subscriber a left join subscriber b on
a.sender = b.receiver and
a.receiver = b.sender


--SQL solution 2
with cte as (select
	sms_date,
        case when (sender < receiver) then sender else receiver end as sender,
        case when (sender > receiver) then sender else receiver end as receiver,
        sms_no
from subscriber)
select
    sms_date,
    sender,
    receiver,
    sum(sms_no)
from cte
group by sms_date, sender, receiver