-- question statement
    -- Find companies where 2 or more user speaks 2 languages English and German
-- create table statement
create table company_users (company_id int, user_id int, language varchar(20));

-- Insert data
insert into company_users values
    (1,1,'English')
    ,(1,1,'German')
    ,(1,2,'English')
    ,(1,3,'German')
    ,(1,3,'English')
    ,(1,4,'English')
    ,(2,5,'English')
    ,(2,5,'German')
    ,(2,5,'Spanish')
    ,(2,6,'German')
    ,(2,6,'Spanish')
    ,(2,7,'English');

-- Input data
"company_id","user_id","language"
1,1,English
1,1,German
1,2,English
1,3,German
1,3,English
1,4,English
2,5,English
2,5,German
2,5,Spanish
2,6,German
2,6,Spanish
2,7,English


-- Required Output
"company_id"
1

--Solution steps
    -- apply filter on English and German to get user speaking these languages
    -- using group by get the users speaking 2 languages
    -- get the cities where this difference is going negative for any days
    -- create temp table with this data
    -- apply group by and having clause to get companies having more than one such users

--SQL solution with CTE and having clause
with users_eng_ger as (
    select
        company_id,
        user_id
    from company_users
    where language in ('English', 'German')
    group by company_id, user_id
    having count(language) > 1)

select company_id
from users_eng_ger
group by company_id
having count(user_id) > 1
