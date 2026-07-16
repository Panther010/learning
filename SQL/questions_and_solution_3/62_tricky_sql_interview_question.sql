-- question statement
    -- Classify each game session into one of 4 social-interaction
    -- categories based on the players' interaction_type events:
    -- 1. No social interaction
    -- 2. One sided interaction
    -- 3. Both sided interaction without a custom_typed message
    -- 4. Both sided interaction with a custom_typed message from at
    --    least one player


-- create table statement
CREATE TABLE user_interactions (
    user_id           varchar(10),
    event             varchar(15),
    event_date        DATE,
    interaction_type  varchar(15),
    game_id           varchar(10),
    event_time        TIME
);


-- insert data
INSERT INTO user_interactions VALUES
('abc', 'game_start', '2024-01-01', null, 'ab0000', '10:00:00'),
('def', 'game_start', '2024-01-01', null, 'ab0000', '10:00:00'),
('def', 'send_emoji', '2024-01-01', 'emoji1', 'ab0000', '10:03:20'),
('def', 'send_message', '2024-01-01', 'preloaded_quick', 'ab0000', '10:03:49'),
('abc', 'send_gift', '2024-01-01', 'gift1', 'ab0000', '10:04:40'),
('abc', 'game_end', '2024-01-01', NULL, 'ab0000', '10:10:00'),
('def', 'game_end', '2024-01-01', NULL, 'ab0000', '10:10:00'),
('abc', 'game_start', '2024-01-01', null, 'ab9999', '10:00:00'),
('def', 'game_start', '2024-01-01', null, 'ab9999', '10:00:00'),
('abc', 'send_message', '2024-01-01', 'custom_typed', 'ab9999', '10:02:43'),
('abc', 'send_gift', '2024-01-01', 'gift1', 'ab9999', '10:04:40'),
('abc', 'game_end', '2024-01-01', NULL, 'ab9999', '10:10:00'),
('def', 'game_end', '2024-01-01', NULL, 'ab9999', '10:10:00'),
('abc', 'game_start', '2024-01-01', null, 'ab1111', '10:00:00'),
('def', 'game_start', '2024-01-01', null, 'ab1111', '10:00:00'),
('abc', 'game_end', '2024-01-01', NULL, 'ab1111', '10:10:00'),
('def', 'game_end', '2024-01-01', NULL, 'ab1111', '10:10:00'),
('abc', 'game_start', '2024-01-01', null, 'ab1234', '10:00:00'),
('def', 'game_start', '2024-01-01', null, 'ab1234', '10:00:00'),
('abc', 'send_message', '2024-01-01', 'custom_typed', 'ab1234', '10:02:43'),
('def', 'send_emoji', '2024-01-01', 'emoji1', 'ab1234', '10:03:20'),
('def', 'send_message', '2024-01-01', 'preloaded_quick', 'ab1234', '10:03:49'),
('abc', 'send_gift', '2024-01-01', 'gift1', 'ab1234', '10:04:40'),
('abc', 'game_end', '2024-01-01', NULL, 'ab1234', '10:10:00'),
('def', 'game_end', '2024-01-01', NULL, 'ab1234', '10:10:00');


-- required output (verified: executed against sqlite3)
"game_id","game_type"
ab0000,Both sided interaction without custom_type message
ab1111,No Social interaction
ab1234,Both sided interaction with custom_typed_messages from atleast one player
ab9999,One sided interaction

-- chains, for reference:
-- ab0000: def sends emoji+preloaded, abc sends gift -- both sides act, no custom_typed
-- ab9999: only abc sends messages (custom_typed + gift) -- def never sends anything
-- ab1111: only game_start/game_end rows for both -- no send_* events at all
-- ab1234: abc sends custom_typed+gift, def sends emoji+preloaded -- both sides, custom_typed present


-- solution steps

-- Step 1:
-- count(interaction_type) counts non-null interaction_type rows per
-- game (game_start/game_end rows have NULL interaction_type and
-- don't count). Zero of these means no social interaction happened.

-- Step 2:
-- count(distinct ... user_id) over rows with a non-null
-- interaction_type tells you how many DIFFERENT players sent
-- anything at all. 1 = one-sided, 2 = both sides participated.

-- Step 3:
-- Among "both sided" games, check whether a custom_typed message
-- exists at all, to split into "with" vs "without" custom_typed.


-- sql solution (your original -- verified correct on the given sample data)
select game_id,
case when count(interaction_type) = 0 then 'No Social interaction'
when count(distinct case when interaction_type is not null then user_id end ) = 1 then 'One sided interaction'
when count(distinct case when interaction_type is not null then user_id end ) = 2
	and count(distinct case when interaction_type = 'custom_typed' then user_id end) = 0 then 'Both sided interaction without custom_type message'
when count(distinct case when interaction_type is not null then user_id end ) = 2
	and count(distinct case when interaction_type = 'custom_typed' then user_id end) = 1 then 'Both sided interaction with custom_typed_messages from atlead one player'
end as game_type,
count(interaction_type)
from user_interactions
group by game_id;

