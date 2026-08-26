Design a system/pipeline to track user activity on e-commese website

Requirements Gathering:
- Functional Requirements
  - Who is the end user.
  - Who is going to consume from this system
    - Marketing analyst -> Batch
    - ML team -> Streaming
    - Product team -> Streaming
  - What they actually need
    - Aggregated matics
    - Raw event
    - Historical snapshow
  - How they are going to access it
    - BI, SQL, Dashboard etc, Rest API
  - Funnel
    - Page view 100000
    - search 60000 (40% drop)
    - view product 30000 (50% drop)
    - add to cart 10000 (67% drop)
    - purchase 4000 (60% drop)
  - Dimension
    - User type new or existing user, Free or paid user
    - Device type desktop or mobile
  - Daily granularity
- Non Functional requirements
  - Latency SLA
    - 1 hour (Batch) or minute or less (Streaming)
  - Volume
    - 1GB (Pandas, Polar), 1TB or 1 PB data (Spark, with partitioning etc)
  - Availability
    - 10 m etc
  - Data Retention
    - Do we keep record forever or move it 


Scenario 1: - CConsumer is marketing team. daily report on behavior. 1 hr data to be refreshed
    - batch. spark. fact dimension

Scenario 2: ML time real time products recommendation
    - Streaming, Kafka, spark streaming, Delta tables


Backoff the envelope calculation:

- Scenario 1
  - Users: 5 M daily user ask interviewer. Each user is going to generate 30 events per session
    - Avg no of session per user = 2
    - Total event /Day = 5m * 2 * 30 = 300 M events/day
    - 1 event = 1 json = {user_id, session_id, timestamp, page_url}
    - 500B tp 1KB = avg 700B
    - Size of 300 M events = 300B * 700B = 210 GB/Day = 6.3 TB/month
    - We need distributed processing in this case
    - for 12 months = 75TB of Deta 
    - With parquest and compression = 2.5 compression = 15-30 TB
    - Partition event-date yyyy/mm/dd
    - No streaming structure is required.
  - Compute engine, 
  - storage format
  - orchestration - airflow
  - Batch processing
    
- Step2 Pipeline design
  - Batch or streaming
  - cost > Latency = batch
  - source -> S3/ADLS
  - Airflow DAG get data from RDBMS to raw/bronze -> cleaning (silver), modeling -> aggregating joining (Gold) 
    
  - Streaming in case latency is under minute
  - Kafka for ingention
  - Spark/flink for processing
  - Delta table for history
  - Redis/dynamodb for 
  - Read by app or dashboard

Example ride-sharing app:
    - Once the ride is completed ride completed event pushed to kafka
    - event contain fare, surge driver etc
    - Spark streaimg will process and write aggregated data to redis
    - app pull from redic

Lambda and Kappa architecture
Lambda architecture mintain 2 system for batch and stream processing
- Two layers    
  - Speed layer
  - Batch Layer
  - Serving layer might or might not be common
  - MSK or kinesis will fatch data FLink or Spark strcutured streaming will process and save it cache or dynamodb
  - Other hand firhose can fatch the data from MSK or kinesis and store in S3
  - EMR and Airflow/step function will run the batch save results in S3
  - Results or batch and stream can produce better results

Kappa Architecture:
    - Every event flow from single pipeline. In case you need historical data replay it from kafka
  - Kafka act as both ingestion and historical data store.
  - any event flow through Kafka and stay there
  - Steaming layer Spark streaming read data from kafka and write it to serving layer
  - In case you need to process historical data. You will create new consumer group
  - Offset will be set for 2 week ago and replay the data and process historical data.



Step 3: Data modeling
1. Medallion architecture:
   - 3 Layer broze, silver, gold
2. Star schema vs Denormalisation 
   - Fact_orders, dim_customer, dim_products
   - De-normalisation: One Big Table: OBT order table, Prejoined table
3. Slowly changing dimension:
   SCD1, SCD2, SCD3
4. Partitioning vs Optimisation:
    - Partitioning primary secondary partitioning
    - Liquid clustering
5. Storage format
   - Parquet vs Avro: Column pruning. Partition pruning. 
     - Read heavy column based and storage
     - Write heavy row based for mostly streaming. 
       - DO not dump a lot of parquet in directory. No ACID consecutive job might corrupt and overwrite the data
       - No schema reinforcement
       - Small file problem
       - Delta lake, Iceberg or Hudi solve these issue
6. Database type:
   - Relational or non-relational
   - Relational: strong consistency, structure data. ACID, join, clear relationship, complex queries
   - Non-relational: Evolving data, flexibility, semi-structure, speed availability

7. Data Quality check:
   - Data quality detention:
     - Completeness
     - Accuracy
     - Consultancy: Data agrees across system
     - Freshness: Data is latest or not. 
     - Uniqueness. 
   - Data quality contract
     - checks dataquality dimension at the time of injection only 
   - Data observability. 

8. Pipeline resilience: 
   - Idempotency
     - Merge instead of insert
   - Backfills:
     - 
9 Schema evalution:
    - Flexible at broze layer
    - Strict at silver and gold layer. Merge schema support it

One Que:
Design a realtime analytics pipeline for food delivery swiggy zomato
1. Consumer -> Restorant partners. Operational dashboard.
2. daily business report requirement

Process start
1. Who are the end users?
   1. Rest partner
   2. Executive teams
2. Latency SLAs
   1. < 2m
   2. 1 day
3. Approx data volume? 
   1. 5 M order a day
   2. 500k/hr
4. What are the event tracked
   1. Order placed
   2. Restaurant confirmed
   3. Driver assigned
   4. Driver picks up
   5. Driver delivered
   6. Cancelled 
5. What is the data retention
   1. 2 Years for analytics
   2. 90 days for real time

Run the math:
- 5 M events per day. 6 events type
- 25-30M event per day
- 30M/24*60*60 almost 350 events per sec
- During 500k/Hr * 6 = 3M per /HR almost 833 per second
- Range is 350-833 per second
- This is manageable for kafka

Storage:
- Each order event is JSON assuming 1KB per event
- 30 M * 1KB = 30GB/day
- 2 Year = 22 TB raw data
- Parquet 4-11 TB
- For real time Streaming layer
  - It do not need complete data 
  - 10-15 fields/restaurants
  - Assume 50K active restaurants
  - 50K * 1k per restant = 50M data


Pipeline design
We are building one data platform 2 consumption pattern
1. Restaurant partner
2. Executive team

- 1 event stram kafka. with 2 path. Lambda style architecture
  - Streaming path -> Real time app min latency
  - Batch path -> Day latency batch processing


Data Modeling

Data Quality Checks
- Data contract at Kafka
  - Valid event type
  - Order-id + event type should not be duplicated
- Silver layer check
  - Null checks
  - Referential integrity check
  - Business rule
    - Delivery duration
  - Volume based check
    - Current order against 7 day rolling avg

Backfill Strategy

Idempotency

Schema evolution
    

















