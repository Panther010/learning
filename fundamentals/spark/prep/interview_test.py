import pyspark.sql import function as F
import pyspark.sql.window import Window
"""
Table 
tx_id, cust_id, country, amount, tx_timestamp
t1,c1,UK,5000, 2026-02-22
t2,c2,USA,7000, 2026-02-23
t3,c1,AUS,1465, 2026-02-24
t4,c1,IND,5432, 2026-02-25
t5,c2,UK,2121, 2026-02-26

- Cust total amount => ()
- TX count
- latest transection amount each customer'
- rank of the customer each country based on total amount

"""
# que1
df.groupBy(
    F.col("cust_id")
).agg(
    F.sum(F.col("amount")).alias("total_amount_by_customer")
)

# que 2
df.count()

# que 3
win_spec = window.partionBy(F.col("cust_id")).orderBy(F.col("tx_timestamp").desc())
result =