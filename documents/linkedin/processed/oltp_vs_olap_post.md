Assuming OLTP can handle analytical workloads without redesign? 🚨  
It forces your OLTP to juggle write‑heavy traffic and ad‑hoc queries, leading to lock contention, slow dashboards, and even outages during peak reporting.

---

### OLTP vs. OLAP – A Quick‑look Comparison

| Feature | OLTP (Row‑Store) | OLAP (Column‑Store) |
|---------|------------------|---------------------|
| Goal | Low‑latency CRUD | High‑throughput analytics |
| Schema | Normalized | Denormalized |
| Storage | Row‑store | Column‑store |
| Transaction model | ACID, high concurrency | Snapshot isolation, batch reads |
| Compression | Low | High |
| Typical workload | Mixed reads/writes | Batch reads, aggregations |

---

#### ASCII Flow Diagram

```
OLTP (Row‑Store)  ──►  CDC  ──►  OLAP (Column‑Store)
      |                    |
      |--- ACID, low latency ──|
```

- OLTP keeps the transactional integrity you rely on.  
- CDC captures every change in real time.  
- OLAP stores a denormalized, column‑oriented copy for fast analytics.

---

Rule of thumb: *Stream changes with CDC, but design separate schemas and storage formats for each layer.*  

🔍 How have you partitioned your data layer to avoid this pitfall? Share your experience!

#OLTP #OLAP #DataArchitecture