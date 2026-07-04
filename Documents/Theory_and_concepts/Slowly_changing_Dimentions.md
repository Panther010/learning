As lead data engineer:
I have created short notes on the basis of my memory and study please review and correct them:
Review and correct where ever required
Add example and details whereever required
Add index which I can use for quick revision
Create the notes in MD format

In data warehousing data is deveident into fact and dimention tables, with time these dimention changes . When these dimention attributes are changeing is directly impact the fates and final anlystics.
If we do not handle them with proper strategy we either lose historical accuracy or ose tract of change in data. In case we keep all the old version data management becomes difficult with huge dimention tables overall processs slows down

- In OLTP system tables simply get updated and with update in row all the transetinal system start reflecting updated values
- Keeping all version increase and create duplicate data.
- SCD type gives startdr and well defined strategy to handle chaging dimetions and thier impact on data

Dimentions tables: Descreptive and reference data tables customer product employee tables
Surrogate key: System generated artifical key used as primary key
Natura business key: real world primary key. Remain constant throught out the history of data.
Effective date/Expirty date: Columnmarking validity of active and inactve version of dimention data
Current flag: Boolen value to reflect active or historical data
Version Number: To tract iteration of change along with date
Late-arriving data: Fat data arrive before the corresponding dimension record

SCD typ0: Never change the attribute it remain immutable once write stay forever.. Chnage is not possible
SCD type1: Simp;y overwrite the changed value. We lose tract of old value and history of changes. It is simple minimal keep data updated but loose tract of history

SCD type2: Add new rowfor latest value and expire ld record either by date or flag value in table
preserve full history. but with time tables grows and become big. 

SCD type3: In case of attribute change in case of new row add new column to store previous value. 
It stores only immediate history data It is relatively simple but preserve only immidiate history no track of historical changes

SCD Type 4: This type maintain 2 table version one for current version and another for historical valu.
This type increases the nuimber of table but solve proble of huge dim tables we do not read to huge dim table it is only trequired in case we want historical dim data rest all the time mostly we fetch latest data. mainenace of 2 tables and ETL complexicity is an issue

SCD tyep6: It is combination of 1,2 and 3(1+2+3):
New row forevery attribute change. But historical records contain additional column containing latest attribute value. Most flexible Spport all kind of data and query. Complex to impliment

Spark implementation

Frequently asked:

What is a Slowly Changing Dimension and why is it needed?
Explain the difference between SCD Type 1, Type 2, and Type 3.
Why do we need surrogate keys for SCD Type 2?
What is a late-arriving dimension and how do you handle it?
How would you implement SCD Type 2 using MERGE INTO in Spark/Delta/Snowflake?

Scenario-based:

A customer's address changes and you need historical sales reports to still reflect the address that was correct at the time of sale — which SCD type would you use and why?
Your SCD Type 2 dimension table has grown to billions of rows and queries are slowing down — how would you redesign it?
You're getting duplicate "current" rows for the same customer in your SCD2 table — what could be causing this and how do you fix it?

Lead Data Engineer design questions:

Design an end-to-end CDC pipeline (source DB → Kafka → Spark/Flink → Delta/Iceberg) implementing SCD Type 2 for a customer dimension at scale.
How would you decide between SCD Type 2 and Type 4 for a dimension with millions of rows and frequent updates?
How do you handle SCD Type 2 in a multi-engine Lakehouse (e.g., Iceberg tables read by Spark, Trino, and Snowflake) while keeping consistent history across all engines?
How would you design dimension versioning to satisfy both business reporting needs and regulatory audit requirements (relevant to financial services)?

Common follow-ups:

How do you handle a fact record that references a dimension key from a row that's since been expired (i.e., how do fact tables join correctly to the right historical version)?
What happens if two changes to the same customer arrive in the same batch — how do you avoid creating rows in the wrong order (out-of-order updates)?
How would you backfill SCD2 history if you're migrating from a system that only kept current-state data?