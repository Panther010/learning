-- question statement
    -- Given friends and likes tables, recommend pages to each user
    -- that at least one of their friends has liked, but that the
    -- user has NOT liked themselves.

-- create table statement
CREATE TABLE friends (
    user_id   INT,
    friend_id INT
);

CREATE TABLE likes (
    user_id INT,
    page_id CHAR(1)
);


-- Insert data
INSERT INTO friends VALUES
(1, 2),
(1, 3),
(1, 4),
(2, 1),
(3, 1),
(3, 4),
(4, 1),
(4, 3);

INSERT INTO likes VALUES
(1, 'A'),
(1, 'B'),
(1, 'C'),
(2, 'A'),
(3, 'B'),
(3, 'C'),
(4, 'B');


-- Input data
"user_id","friend_id"
1,2
1,3
1,4
2,1
3,1
3,4
4,1
4,3

"user_id","page_id"
1,A
1,B
1,C
2,A
3,B
3,C
4,B


-- Required Output (verified: executed against sqlite3)
"user_id","page_id"
2,B
2,C
3,A
4,A
4,C

-- reasoning per user:
-- user1: friends 2,3,4 like {A},{B,C},{B} -> union {A,B,C} -- user1
--         already likes all of A,B,C -> no recommendations
-- user2: friend 1 likes {A,B,C} -- user2 already likes A ->
--         recommend B, C
-- user3: friends 1,4 like {A,B,C},{B} -> union {A,B,C} -- user3
--         already likes B,C -> recommend A
-- user4: friends 1,3 like {A,B,C},{B,C} -> union {A,B,C} -- user4
--         already likes B -> recommend A, C


-- solution steps

-- Step 1:
-- Join friends to likes on friend_id = likes.user_id -- this gives,
-- for every (user, friend) pair, every page that friend has liked.
-- This is the full candidate set of "pages a friend likes."

-- Step 2:
-- Left join that candidate set back to likes, this time matching on
-- the ORIGINAL user (not the friend) and the same page_id. If this
-- join finds a match, the user already likes that page -- exclude
-- it. If it finds NO match (right side NULL), the user has never
-- liked that page -- recommend it.

-- Step 3:
-- DISTINCT collapses duplicates that naturally arise when multiple
-- friends like the same page (e.g. user4's friends 1 and 3 both like
-- page C -- without DISTINCT this would double-count).


-- sql solution1
with cte as (
select
	f.user_id, f.friend_id, l.page_id
from friends f
join likes l on f.friend_id = l.user_id
order by f.user_id)
select distinct c.user_id, c.page_id
from cte c
left join likes l1
    on c.user_id = l1.user_id
   and c.page_id = l1.page_id
where l1.user_id is null;


-- sql solution 2
select distinct f.user_id, l.page_id
from friends f
join likes l on f.friend_id = l.user_id
where not exists (
    select 1 from likes l2
    where l2.user_id = f.user_id
      and l2.page_id = l.page_id
);
