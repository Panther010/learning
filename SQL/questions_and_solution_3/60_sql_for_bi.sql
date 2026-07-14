CREATE TABLE calendar_dim (
    date_key INT PRIMARY KEY,                  -- Format: YYYYMMDD (Ideal for indexing/joins)
    full_date DATE NOT NULL,                   -- Standard DATE type
    year_num INT NOT NULL,                     -- e.g., 2026
    quarter_num INT NOT NULL,                  -- 1 to 4
    quarter_name CHAR(2) NOT NULL,             -- Q1, Q2, Q3, Q4
    month_num INT NOT NULL,                    -- 1 to 12
    month_name VARCHAR(10) NOT NULL,          -- January, February
    month_short_name CHAR(3) NOT NULL,         -- Jan, Feb
    week_of_year INT NOT NULL,                 -- 1 to 53
    day_num INT NOT NULL,                      -- Day of the month: 1 to 31
    day_of_week INT NOT NULL,                  -- 1 (Monday) to 7 (Sunday)
    day_name VARCHAR(10) NOT NULL,             -- Monday, Tuesday
    is_weekend BOOLEAN NOT NULL,                -- TRUE/FALSE
    todays_year INT not NULL
);

INSERT INTO calendar_dim
SELECT
    TO_CHAR(datum, 'YYYYMMDD')::INT AS date_key,
    datum AS full_date,
    EXTRACT(YEAR FROM datum) AS year_num,
    EXTRACT(QUARTER FROM datum) AS quarter_num,
    'Q' || EXTRACT(QUARTER FROM datum) AS quarter_name,
    EXTRACT(MONTH FROM datum) AS month_num,
    TO_CHAR(datum, 'Month') AS month_name,
    TO_CHAR(datum, 'Mon') AS month_short_name,
    EXTRACT(WEEK FROM datum) AS week_of_year,
    EXTRACT(DAY FROM datum) AS day_num,
    EXTRACT(ISODOW FROM datum) AS day_of_week,
    TO_CHAR(datum, 'Day') AS day_name,
    CASE WHEN EXTRACT(ISODOW FROM datum) IN (6, 7) THEN TRUE ELSE FALSE END AS is_weekend,
    extract(year from current_date)
FROM
    -- Change the start and end dates below to fit your dataset's range
    GENERATE_SERIES('2020-01-01'::DATE, '2030-12-31'::DATE, '1 day'::INTERVAL) AS datum;


select * from calendar_dim