-- create table statement
    --Loaded data from the file "Superstore_orders.csv" present in data section
-- Insert data
    --Loaded data from the file "Superstore_orders.csv" present in data section

-- Input data

-- Required Output
    -- Write a query to prove pareto principle
    -- 80% sales comes from the 20% of the products

--Solution steps
    -- create a sub table with product_id and total sale amount of the product using CTE
    -- Once created calculate following columns:
        --running sales total or the products using sum() window function
        --80 % of total sales using sum window function with empty over() clause
        --Total product count with count() window function
        --running product count using row number
        --running percentage using running product count and total product count
        -- difference between 80 % sale and running sales
    --by this query we can see around 22% product are contributing to 80% of the sale

--SQL solution1
with product_sales_total as (
	select product_id,
		sum(sales) as product_sales,
		sum(profit) as product_profit
		from superstore_orders so
	group by product_id
	order by sum(sales) desc)

select product_id,  product_sales,
sum(product_sales) over(order by product_sales desc) as running_sale_total,
.8 * sum(product_sales) over() as total_sales_80_percent,
count(product_id) over() as total_product_count,
(row_number() over(order by product_sales desc)  * 100) / (count(product_id) over()) as running_percentage,
row_number() over(order by product_sales desc) as running_product_count,
.8 * sum(product_sales) over() - sum(product_sales) over(order by product_sales desc) as sale_difference
from product_sales_total


