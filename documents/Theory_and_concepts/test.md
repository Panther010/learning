Your app just crashed because you ran a full table scan on a live order‑processing system.  
In production, the OLTP vs. OLAP trade‑off isn’t a theory—it’s the difference between 1 ms latency and a 5‑minute wait.  

**What you need to know**

🔹 **Data layout**  
• OLTP: row‑oriented, 8‑16 KB pages, 3rd‑normal‑form.  
• OLAP: columnar (Parquet, Delta), star/snowflake or wide tables.  

🔹 **Work‑load focus**  
• OLTP: high‑concurrency, low‑latency reads/writes, strict ACID, vertical scaling.  
• OLAP: read‑heavy, high‑throughput, latency measured in seconds/minutes, horizontal scaling.  

🔹 **Storage & compression**  
• Row store: fast single‑row access, less compression.  
• Column store: high compression, I/O savings, great for aggregations.  

🔹 **Data movement**  
• CDC (Change Data Capture) + ELT/ETL bridges the two worlds.  
• Write changes in OLTP → stream to a lake → load into an OLAP warehouse.  

**Rule of thumb**  
Keep write‑heavy, transactional data in a normalized, row‑oriented store; move analytical workloads to a denormalized, columnar format.  

How do you decide where a new feature belongs—transactional or analytical?

#OLTP #OLAP #CDC