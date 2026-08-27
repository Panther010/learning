# Kafka & Streaming — Complete Revision Notes
*(Organized in the order you'd realistically want to learn this: Kafka fundamentals → streaming concepts → Spark Structured Streaming implementation)*

---

# PART 1 — Kafka Fundamentals

## 1. What Is Apache Kafka?

**Apache Kafka** is an **open-source, distributed event-streaming platform**. In plain terms: it's a super-fast, reliable "post office" that collects data/events from many different systems in real time, and lets other systems read that data — all at very high speed and scale.

- **Collects/integrates data streams** — pulls events from many different source systems into one central place.
- **Processes real-time event streams** — data flows through continuously, not in one big daily batch.
- **Highly scalable** — handles huge volumes by spreading work across many machines (brokers).

> Example: An e-commerce site has orders, page-views, and payment events happening every second across different services. Kafka acts as the **central nervous system** collecting all these events, so downstream systems (fraud detection, analytics, recommendations) can all consume the same stream independently.

---

## 2. Core Architecture — Producer, Broker, Consumer

Kafka works on the principle of a **message queue** — producers drop messages in, consumers pick them up.

| Part                 | Role                                                                                                                                                           |
|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Producer (API)**   | Sends/publishes data (events) **into** a Kafka broker.                                                                                                         |
| **Broker (Cluster)** | The actual Kafka server(s) that **store and manage** incoming data streams. Multiple brokers together form a **cluster**, for scalability and fault tolerance. |
| **Consumer (API)**   | Reads/receives data **from** the broker for downstream processing.                                                                                             |

> Example use case: In a microservices architecture, an "order placed" event triggers inventory, billing, and notification services simultaneously — each consuming the same Kafka stream independently, without calling each other directly. This **decouples** services from one another.

---

## 3. Topics, Partitions, Offsets & Consumer Groups

These four concepts are the real heart of how Kafka scales and organizes data — worth knowing in depth.

**Topic**
A named "channel"/category that events are published to (e.g., `orders`, `payments`). Producers write to a topic; consumers read from it. Think of it as a labeled folder for one type of event.

**Partition**
Each topic is split into **partitions** so data can be spread across brokers and read **in parallel** — this is *how* Kafka achieves scale.
- More partitions = more parallelism = higher throughput (up to a point).
- Kafka guarantees message **order only within a single partition**, *not* across an entire topic.
- Producers decide which partition a message goes to — usually by hashing a **message key** (e.g., `customer_id`). Same key → always the same partition → order preserved for that key.
> Example: If strict order matters for all events belonging to one customer, use `customer_id` as the message key — Kafka will always route that customer's events to the same partition, keeping them in order.

**Offset**
A unique, ever-increasing ID for each message **within a partition**, marking its position (like a line number in a log file). Consumers track offsets to know what they've already read, and can also intentionally "seek" to an earlier or later offset (e.g., to replay old data).

**Consumer Group**
A set of consumers working together to read a topic, splitting the partitions between them so **no two consumers in the group read the same message twice**.
- Each partition is only consumed by **one** consumer within a group at a time.
- Multiple consumer groups can independently read the *same* topic in full — groups don't affect each other.
- **Rebalancing** — when a consumer joins or leaves a group (e.g., crashes, scales up), Kafka automatically **redistributes partitions** among the remaining consumers in that group.

> Simple analogy: **Topic** = a mailbox for one type of letter. **Partition** = multiple mail slots within that mailbox, so several people can sort mail at once. **Offset** = the position of a specific letter in a slot. **Consumer Group** = a team of people splitting up the slots so nobody reads the same letter twice.

---

## 4. Replication & Durability (ISR)

Kafka protects against data loss by **replicating** each partition across multiple brokers.

- Each partition has one **leader** replica (handles all reads/writes) and one or more **follower** replicas (copy data from the leader).
- **ISR (In-Sync Replicas)** — the set of replicas that are fully caught up with the leader at any given moment. If the leader broker dies, Kafka promotes one of the in-sync followers to be the new leader — **no data loss**, as long as at least one in-sync replica exists.
- **Replication factor** — how many total copies of each partition exist (e.g., replication factor 3 = the leader + 2 followers). Higher = more durable, but more storage/network cost.

---

## 5. Delivery Semantics & Ordering Guarantees

**Delivery Semantics** — how many times a message is guaranteed to be processed:

| Semantic          | Meaning                                                            | Risk                                                                                                                              |
|-------------------|--------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| **At-most-once**  | Each message processed **0 or 1 times** — never retried.           | Risk of **data loss**.                                                                                                            |
| **At-least-once** | Each message processed **1 or more times** — retried on failure.   | Risk of **duplicates**.                                                                                                           |
| **Exactly-once**  | Each message processed **exactly 1 time**, regardless of failures. | Hardest to achieve — usually built from **at-least-once + idempotence** working together, rather than being one single mechanism. |

**Producer-side reliability controls:**
- **`acks` setting** — how many broker replicas must confirm receipt before the producer considers a send "successful":
  - `acks=0` — fire and forget (fastest, least safe).
  - `acks=1` — leader broker confirms only (default balance).
  - `acks=all`/`-1` — all in-sync replicas confirm (safest, slowest).
- **Idempotent Producer** (`enable.idempotence=true`) — Kafka tags each message with a producer ID + sequence number, so the broker automatically **drops duplicate sends** caused by producer retries.
- **Kafka Transactions** — allow a producer to write to multiple partitions/topics **atomically** (all succeed or all fail together) — this is what enables true **exactly-once** semantics across multiple topics, often paired with "read-process-write" pipelines (e.g., Kafka Streams).

**Ordering Guarantee**
Kafka only guarantees order **within a single partition** — never across a whole topic. If order matters for a specific entity, always key messages by that entity's ID (see Partitions above).

---

## 6. Retention & Log Compaction

Kafka doesn't store data forever by default — you control how long.

- **Time/size-based retention** — the default: messages are deleted after a configured time period (e.g., 7 days) or once the log exceeds a size limit — regardless of whether they've been consumed.
- **Log Compaction** — an alternative retention strategy that keeps only the **latest value per key**, discarding older values for that same key instead of deleting by age. Useful for topics representing "current state" rather than a full event history.
  > Example: A topic tracking `customer_id → current_address`. You don't need every historical address change kept forever — compaction keeps just the latest one per customer, saving space.

---

## 7. Schema Registry & Schema Evolution

Real-world event streams change shape over time (new fields added, types changed) — this risks **breaking consumers** if a producer suddenly sends an unexpected format.

- **Schema Registry** (commonly **Confluent Schema Registry**) — a separate service that stores the *agreed-upon* structure (schema) for each topic, typically using **Avro**, **Protobuf**, or **JSON Schema**.
- Producers/consumers validate against the registry to ensure new data is **compatible** with the existing schema (e.g., adding an optional field is fine; removing a required one isn't) before it's allowed through.
- Prevents a schema change on the producer side from silently breaking every downstream consumer.

> Not always needed for small/simple pipelines, but becomes essential once multiple teams/systems depend on the same topic in production.

---

## 8. Consumer Lag (Monitoring)

**Consumer Lag** = the gap between the latest offset written to a partition and the offset a consumer has actually processed.

- High/growing lag = your consumers are **falling behind** the rate of incoming data — a key operational health signal.
- Monitored continuously in production (e.g., via Kafka's own tooling or platforms like Burrow/Confluent Control Center) to catch pipelines that are silently falling behind before it becomes a bigger problem.

---

## 9. Kafka Setup — Docker Containers

A common local/dev setup runs Kafka using **two Docker containers**:

| Container        | Purpose                                                                                                                                                            | Default Port |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| **ZooKeeper**    | Manages broker metadata — tracks which brokers are alive, cluster configuration, and leader election for partitions. (Required in traditional/older Kafka setups.) | `2181`       |
| **Kafka Broker** | The actual Kafka server that stores and serves event data.                                                                                                         | `9092`       |

An **External Application** (your producer/consumer code) then connects to the broker on port `9092` to send/receive events.

> 📌 **Good to know:** Kafka 3.3+ supports **KRaft mode**, which **removes the ZooKeeper dependency entirely** — brokers manage metadata themselves. A modern setup with just one container type (no ZooKeeper) is running KRaft mode. ZooKeeper + Broker (two containers) is still very common in tutorials and legacy deployments.

---

# PART 2 — Core Streaming Concepts

## 10. Designing a Streaming Job — Key Considerations

Before building any streaming pipeline, think through **job frequency** — how often it runs, and whether that's "batch-like" (every few minutes) or truly continuous. This raises several design questions:

- **Each iteration must finish within its frequency window** — if a job runs every 2 minutes but takes 5 to process, iterations start piling up/overlapping.
- **Handling data volume spikes** without breaking the pipeline.
- **Cleanup & housekeeping** — old files, temp checkpoints, processed data need managing so storage doesn't grow forever.
- **Backpressure** — data arriving **faster** than it can be processed; the system needs to slow intake or buffer safely rather than crash or lose data.
- **Scheduling vs. continuous listening** — trigger on a fixed schedule (via an orchestrator) or run a process that's **always on**, listening for new data?
- **Incremental processing** — only process *new* data each run (via checkpointing, Delta Lake, etc.), not everything from scratch.
- **Failure handling** — can a failed micro-batch retry safely, without duplicating or losing data?
- **Late-arriving records** — data showing up after its "expected" window (see §14).

**Orchestration Tool**
A tool that schedules, monitors, and manages execution of data jobs/pipelines — handling dependencies, retries, alerting, and timing (e.g., **Apache Airflow**, **Databricks Workflows**, **Dagster**). Rather than running jobs manually, an orchestrator decides *when* and *in what order* things run, and what to do if one fails.

---

## 11. Stateless vs. Stateful Processing

Whether an operation needs to **remember anything** about past data to process the current record.

**Stateless Processing**
Each record is handled **independently** — no memory of previous records needed.
> Example: Filtering out `status = "error"` events, or converting Celsius to Fahrenheit.
- **Implementation:** `filter()`, `select()`, `withColumn()`, `map()`.
- **Pros:** Simple, cheap, scales easily, fast recovery after failure.
- **Cons:** Can't answer questions like "what's the running total?"

**Stateful Processing**
The operation needs to **remember information across records/batches**.
> Example: A running count of orders per customer, a 5-minute rolling average, or "has this user logged in 3+ times today?"
- **Implementation:** aggregations (`groupBy().count()`), windowed operations, `mapGroupsWithState`, stream-stream joins.
- Spark keeps this "state" in a **state store**, backed by the checkpoint location, so it survives restarts.
- **Pros:** Enables real analytics — aggregates, trends, patterns.
- **Cons:** State grows over time (needs watermarking to bound it), heavier resource usage, harder to reshuffle/scale, more involved recovery after failure.

> Remember it as: **Stateless = "each record on its own island."** **Stateful = "records need to talk to their past selves,"** which means something has to store that history.

---

## 12. Event Time vs. Processing Time

A foundational distinction for everything that follows:

- **Event time** — when something actually *happened* (e.g., a sensor reading logged at 12:00:00).
- **Processing time** — when your system actually *sees/processes* it (e.g., 12:07:00, due to a network delay).

**Late data** = event time is significantly earlier than processing time. Common causes: mobile/IoT devices going offline and syncing later, network delays, upstream retries, clock skew between systems.

---

## 13. Windowing — Grouping Events Over Time

Windows group events that happen **close together in time** — essential for stateful operations like "count per 5-minute window."

**1. Tumbling Window** — fixed-size, **non-overlapping**, back-to-back. Every event belongs to exactly **one** window.
```python
df.groupBy(window("event_time", "5 minutes")).count()
```
- **Pros:** Simple, each event counted exactly once. **Cons:** Can split a burst of activity across a boundary. **Usage:** periodic reporting (orders per 5 min, hourly aggregates).

**2. Sliding Window** — fixed-size, **overlapping**, advancing by a smaller "slide" interval. One event can belong to multiple windows.
```python
df.groupBy(window("event_time", "10 minutes", "5 minutes")).count()
```
- **Pros:** Smoother trend detection (moving averages), avoids hard cutoffs. **Cons:** More compute/state overhead. **Usage:** moving averages, smoothing noisy metrics.

**3. Session Window** — **dynamic-length**, based on actual activity gaps rather than a fixed clock. Stays "open" while events keep arriving within a gap threshold; "closes" after a period of inactivity.
```python
df.groupBy(session_window("event_time", "10 minutes")).count()
```
- **Pros:** Naturally maps to real user/device behavior. **Cons:** Unpredictable size, harder to bound state. **Usage:** user session analytics, clickstream analysis.

> Quick comparison: **Tumbling** = fixed, no overlap, simplest. **Sliding** = fixed, overlapping, smoother trends. **Session** = variable length, driven by activity gaps.

---

## 14. Watermarking & Late Data Handling

**Watermark** = a moving threshold telling Spark: *"I'll wait up to X time for late data, but after that, I'll consider the window closed and stop waiting."*
```python
df.withWatermark("event_time", "10 minutes") \
  .groupBy(window("event_time", "5 minutes")) \
  .count()
```
This means: *group events into 5-minute windows, but allow data up to 10 minutes late before finalizing and dropping a window's state.*

**Why it's needed**
Without a watermark, Spark would have to keep **all past state forever**, since a "late" record could theoretically arrive at any time — memory grows unbounded and the job eventually fails.

**The real trade-off**

| Watermark     | Effect                                                                                                             |
|---------------|--------------------------------------------------------------------------------------------------------------------|
| Too **short** | More late data dropped → less accurate, but low memory usage and low latency.                                      |
| Too **long**  | Captures more late data → more accurate, but higher memory/state usage and higher latency before results finalize. |

**Ways to handle late data in practice**

| Approach                                          | How it works                                                                                            | Trade-off                                                                          |
|---------------------------------------------------|---------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| **Watermarking**                                  | Define lateness tolerance; state is kept that long, then finalized and dropped.                         | Simple, bounded memory — but anything later than the threshold is dropped.         |
| **`Update` output mode**                          | Instead of `Append`, use `Update` so a late record can **revise** an already-emitted window result.     | Needs a sink that supports updates/upserts (e.g., Delta `MERGE`), not a flat file. |
| **Wider watermark/buffer**                        | Increase lateness tolerance if data is often late.                                                      | More accurate, but more state kept longer = more resources.                        |
| **Dead-letter / side-output for "too-late" data** | Route records past the watermark to a separate "late arrivals" table instead of silently dropping them. | Extra complexity, but nothing is lost — can be reviewed/reprocessed later.         |

> Example: An IoT sensor pipeline sets a 10-minute watermark. A sensor goes offline and reconnects 30 minutes later, dumping its backlog — those readings are now past the watermark and get dropped, unless a dead-letter path is set up to catch them.

**Key trade-off to remember:** it's always a choice between **(1)** dropping some late data to keep things simple and bounded, or **(2)** accepting extra complexity/state/cost to capture it more fully.

---

## 15. Idempotence & Exactly-Once Processing

**What is Idempotence?**
An operation is **idempotent** if running it once or multiple times produces the **exact same end result**. This matters constantly in streaming because retries, restarts, and failures are *normal*, not edge cases.

**The Problem Without It**
Streaming systems typically default to **at-least-once** delivery (safer to resend than silently drop). This means:
- If a micro-batch fails **after** writing data but **before** the checkpoint commits, restart causes Spark to **reprocess that same batch again**.
- Without idempotence → **duplicate records** (e.g., a payment processed twice).

> Example: A job writes "Order #123 shipped," crashes right after, before checkpointing. On restart it reprocesses the same event and writes "Order #123 shipped" again — now the system thinks it shipped twice.

**How to Achieve It**

| Technique                               | How it works                                                                                                                     |
|-----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| **Unique keys + Upsert (Merge)**        | Use a unique ID (`order_id`, or `topic+partition+offset`) and `MERGE INTO`/upsert: "insert if new, overwrite if exists."         |
| **Idempotent Kafka Producer**           | `enable.idempotence=true` — broker auto-drops duplicate sends from producer retries.                                             |
| **`dropDuplicates()` + watermark**      | Track a unique event ID within a bounded time window and drop already-seen rows.                                                 |
| **Idempotent sink design**              | A unique constraint on the destination table so a duplicate insert simply fails/no-ops.                                          |
| **Checkpointing + transactional sinks** | Sinks with atomic/exactly-once writes (Delta Lake, Kafka transactions) so a write + checkpoint commit happen as one atomic unit. |

**Pros:** safe retries, exactly-once-*like* behavior on top of at-least-once delivery, simpler crash recovery.
**Cons:** extra overhead (tracking IDs, merge/upsert cost), dedup state itself needs memory + cleanup, and it's **not automatic** — must be deliberately designed in.

---

## 16. Checkpointing — Deep Dive

**How it works**
On every micro-batch, Spark writes to the checkpoint location (durable storage, e.g., cloud storage):
- **Offsets/progress** — exactly which data has been read/processed.
- **State store snapshots** — for stateful ops, the actual aggregation/join state needed to resume correctly.
- **Query metadata** — configuration used, for consistency on restart.

On restart/failure, Spark reads the checkpoint and **resumes exactly where it left off**.

**Pros:** enables fault tolerance, lets stateful processing survive restarts, and — combined with idempotent sinks — gets you close to exactly-once behavior.

**Cons/Trade-offs:**
- **Storage overhead**, growing with state size.
- **Can't casually change query logic** after a checkpoint exists (e.g., changing aggregation keys can force starting a fresh checkpoint).
- Slight per-batch performance cost.
- Must live on **reliable, durable storage** — losing it means losing the ability to recover cleanly.

> Rule of thumb: **never delete or move a checkpoint directory** for a running production job unless you deliberately intend to reset and reprocess from scratch.

---

## 17. Backfilling — Reprocessing Historical/Missed Data

**What is Backfilling?**
Running a pipeline over **past data** that was never processed, or needs reprocessing — as opposed to normal streaming, which only handles new incoming data.

**Common reasons**
- A pipeline was down and missed a chunk of data (**gap-filling**).
- A bug in transformation logic was fixed, and historical output needs correcting.
- A new feature/column is added, and you want it applied retroactively.
- **Initial load** — bringing a brand-new pipeline up to date with everything that existed before it started.

**Why It's Tricky**
- **Duplicate risk** — overlapping with what the live stream already processed; needs idempotent writes to avoid double-counting.
- **Watermark conflicts** — if backfill data is fed into the *same* live query, the watermark (based on current event times) has likely moved far ahead, so old backfill data may be immediately treated as "too late" and dropped.
- **Resource spikes** — reprocessing months of history at once is far heavier than a normal micro-batch.
- **Ordering/consistency** — a live pipeline running *at the same time* as a backfill shouldn't write to overlapping time ranges simultaneously.
- **Schema mismatches** — old data may not match the current schema (missing columns, different types).

**How It's Typically Done**
1. **Run it as a separate batch job**, not inside the live stream — use `spark.read` (batch, not `readStream`) over the historical range, apply the same transformation logic, and write via **idempotent merge/upsert**.
2. **`Trigger.AvailableNow`** — point the job at historical data and let it process everything available once, then stop; reuses existing streaming logic.
3. **Use a separate checkpoint location** for the backfill run — reusing the live job's checkpoint can confuse offset tracking between the two runs.
4. **Kafka offset/timestamp reset** — set `startingOffsets` to `"earliest"` or a specific timestamp to replay historical Kafka data (as long as retention hasn't expired it).
5. **Delta Lake time travel** (`VERSION AS OF` / `TIMESTAMP AS OF`) — query a table as of a previous state, useful for backfilling from a known snapshot.
6. **Write to a staging table first, then merge** — validate correctness before merging into production.

> Rule of thumb: **treat backfilling as a batch problem, not a streaming problem** — reuse the pipeline's transformation logic, but run it as a one-time/scheduled batch job with its own checkpoint and idempotent writes, rather than injecting old data into a live continuous stream.

---

# PART 3 — Spark Structured Streaming (Implementation)

## 18. Basics — `readStream` / `writeStream` & the Micro-Batch Model

Spark treats a stream as **an ever-growing table** — new data keeps getting appended, processed incrementally.

- **`spark.readStream`** — reads data as a continuous stream (vs. `spark.read` for a one-time static batch).
- **`.writeStream`** — writes the processed stream output somewhere, continuously.

**The Micro-Batch Cycle**
1. The **Streaming Query** continuously watches the source for new incoming data.
2. As soon as new data lands, it **updates its checkpoint** and **triggers a micro-batch**.
3. `readStream` reads the new data → transformations applied → `writeStream` writes the result.
4. The **checkpoint is committed** (marking this data "processed").
5. The query goes back to **watching for the next batch**, and the cycle repeats.

> Think of a mail carrier who checks the mailbox, and every time new mail appears, immediately picks it up, processes it, delivers it, then notes "delivered up to here" before checking again.

This gives **near real-time processing** with the reliability/simplicity of batch processing under the hood.

---

## 19. Triggers — Controlling *When* Micro-Batches Run

**1. Unspecified (Default)** — a new micro-batch starts immediately after the previous one finishes ("as fast as possible").

**2. Fixed Interval** — micro-batches kick off at a user-specified interval, regardless of how long the previous batch took.
```python
df.writeStream \
  .format("delta") \
  .option("checkpointLocation", "<path>") \
  .trigger(processingTime='2 seconds') \
  .table("<table_name>")
```

**3. Available Now** — a one-time trigger that processes all currently available data (possibly across several internal micro-batches), then **stops on its own**.
- Great for **cost savings** — no cluster running 24/7 just to "listen."
- Effectively turns streaming logic into a scheduled **incremental batch** job.

> Comparison: **Unspecified** = "keep going nonstop." **Fixed Interval** = "check in every X seconds." **Available Now** = "process what's here right now, then stop."

*(Bonus: Spark also has an experimental* **Continuous Processing** *trigger for true millisecond-level latency instead of micro-batches — more limited, less commonly used.)*

---

## 20. Output Modes

How Spark writes the result table each time it updates:

| Mode         | Meaning                                                        | Typical use                                                                      |
|--------------|----------------------------------------------------------------|----------------------------------------------------------------------------------|
| **Append**   | Only **new rows** since the last trigger are written.          | Simple streaming, raw events with no aggregation.                                |
| **Update**   | Only rows that **changed** since the last trigger are written. | Aggregations where existing groups can update (e.g., running counts).            |
| **Complete** | The **entire result table** is rewritten every trigger.        | Small aggregations needing a full up-to-date picture (e.g., a live leaderboard). |

> Not every mode works with every query — e.g., **Append** isn't allowed with certain aggregations unless a watermark is defined, since Spark needs to know when a row is truly "final."

---

## 21. Sources & Sinks

**Source** = where streaming data comes **from**. **Sink** = where it goes **to**.

| Sources (input)  | Sinks (output)                               |
|------------------|----------------------------------------------|
| File/Directory   | File/Directory                               |
| Delta Table      | Delta Table                                  |
| Kafka            | Kafka                                        |
| Other connectors | `foreach` (custom row-by-row logic)          |
|                  | `foreachBatch` (custom batch logic, see §25) |
|                  | Other connectors                             |

> `foreach` lets you write custom logic for handling each row/batch of output (e.g., pushing to a REST API), instead of using a built-in connector.

---

## 22. Rate Limiting (Controlling Backpressure)

Directly answers the "backpressure" problem raised in §10 — Spark lets you cap how much data enters a single micro-batch:

- **`maxOffsetsPerTrigger`** (Kafka source) — caps how many Kafka messages are pulled per micro-batch.
- **`maxFilesPerTrigger`** / **`maxBytesPerTrigger`** (file source) — caps how many new files (or how much data) are picked up per micro-batch.

> Example: A huge backlog of files suddenly appears. Setting `maxFilesPerTrigger=100` processes them gradually, 100 at a time per batch, instead of one massive batch that could exhaust memory.

---

## 23. Cleaning the Source Directory (File-based Streams)

```python
.option("cleanSource", "delete")
```
Deletes the source file entirely once processed.

```python
.option("cleanSource", "archive")
.option("sourceArchiveDir", "<path>")
```
Moves the processed file to an archive directory instead — safer, keeps a copy for auditing/reprocessing.

---

## 24. Naming a Streaming Query

```python
.queryName("name_of_the_query")
```
Gives your streaming query a human-readable name — much easier to identify in the Spark UI/logs when running multiple queries at once (otherwise they show up as auto-generated IDs).

---

## 25. `foreachBatch` — Custom Batch Logic Per Micro-Batch

Lets you treat each micro-batch as a plain **static DataFrame** and run *any* normal batch logic on it — multiple sink writes, custom `MERGE INTO`, dedup logic not natively supported as a streaming sink. This is the practical glue that ties together idempotent writes, DLQ handling, and backfill patterns.
```python
def write_batch(batch_df, batch_id):
    batch_df.write.format("delta").mode("append").save("<path>")

df.writeStream.foreachBatch(write_batch).start()
```

---

## 26. Handling Malformed Records ("Poison Pills") & Dead Letter Queues

Real streams eventually contain a record that breaks parsing/transformation logic (bad JSON, unexpected type, corrupt bytes). Unhandled, this can **crash the entire streaming query**.

- **`badRecordsPath`** or parse modes (`PERMISSIVE` / `DROPMALFORMED` / `FAILFAST`) — route unparseable records to a separate location instead of failing the whole job.
- **Dead Letter Queue (DLQ) pattern** — inside `foreachBatch`, wrap logic in error handling so a bad record gets written to a separate "quarantine" table/topic for later inspection, while good records keep flowing normally.

> Example: A record with an unparseable timestamp goes to a `bad_records` table instead of stopping the entire pipeline.

---

## 27. Monitoring Streaming Queries

Production pipelines need visibility into health, not just "is it running":

- **Input rate vs. processing rate** — if input consistently outpaces processing, backpressure is building up.
- **Batch duration** — sudden spikes suggest resource issues or an oversized/skewed batch.
- **`StreamingQueryListener`** — Spark API to hook into query start/progress/termination events for custom alerting/logging (e.g., a Slack alert if a query stops unexpectedly).

---

## 28. Stream-Stream & Stream-Static Joins

Joining two live streams together (e.g., matching "ad clicks" with "ad impressions") is much harder than a normal join — Spark has to decide *how long* to wait for a matching record on the other side. This is exactly where **watermarks become required**, not just optional, so Spark knows when it's safe to give up waiting on a match.

---

## 29. Auto Loader (Bonus — Databricks-Specific)

A Databricks feature (`cloudFiles` source) built for **incrementally and efficiently ingesting new files** from cloud storage:
- Automatic **schema inference & evolution** — adapts as new columns appear over time.
- Efficient file discovery — avoids expensive full-directory listing on every batch, even at huge scale.
- Native **backfill support** via a `backfillInterval` option that periodically re-scans in case files were missed by normal incremental listing.

---

## Quick Recap Table

| Term                                      | One-liner                                                                      |
|-------------------------------------------|--------------------------------------------------------------------------------|
| Kafka                                     | Distributed platform for collecting & processing real-time event streams       |
| Producer / Broker / Consumer              | Sends data → stores/manages data → reads data                                  |
| Topic / Partition / Offset                | Channel → parallel split of channel → position marker within it                |
| Consumer Group                            | Set of consumers splitting a topic's partitions, no double-reads               |
| Rebalancing                               | Kafka redistributes partitions when consumers join/leave a group               |
| Replication / ISR                         | Copies of a partition across brokers; ISR = replicas fully caught up           |
| acks (producer)                           | How many replicas must confirm before a send is "successful"                   |
| Idempotent Producer                       | Kafka auto-drops duplicate sends from producer retries                         |
| Kafka Transactions                        | Atomic multi-partition/topic writes — enables true exactly-once                |
| Retention / Compaction                    | Delete by age/size, or keep only latest value per key                          |
| Schema Registry                           | Central store enforcing compatible schemas across producers/consumers          |
| Consumer Lag                              | How far behind a consumer is from the latest data — key health metric          |
| ZooKeeper / KRaft                         | Manages broker metadata (older setups) / brokers self-manage (newer)           |
| Backpressure                              | Data arriving faster than it can be processed                                  |
| Stateless Processing                      | Each record handled independently, no memory needed                            |
| Stateful Processing                       | Operation needs memory of past records (aggregates, joins, windows)            |
| Event Time vs Processing Time             | When something happened vs. when your system actually saw it                   |
| Tumbling / Sliding / Session Window       | Fixed no-overlap / fixed overlapping / activity-gap-based windows              |
| Watermark                                 | Threshold for how long to wait for late data before closing a window           |
| Idempotence                               | Same operation run multiple times = same end result (no duplicates)            |
| At-most/least/exactly-once                | Delivery guarantees on how many times a message gets processed                 |
| Checkpointing                             | Stores offsets + state snapshots so a job resumes exactly where it left off    |
| Backfilling                               | Reprocessing historical/missed data — best done as an idempotent batch job     |
| Micro-batch                               | Spark's model: watch → trigger → process → commit checkpoint → repeat          |
| Trigger: Unspecified/Fixed/Available Now  | Nonstop / every X seconds / process-once-then-stop                             |
| Output Modes                              | Append (new rows) / Update (changed rows) / Complete (full table)              |
| Source / Sink                             | Where streaming data comes from / goes to                                      |
| maxOffsetsPerTrigger / maxFilesPerTrigger | Rate-limit how much data enters one micro-batch                                |
| cleanSource                               | Auto-delete or archive files after they're processed                           |
| queryName                                 | Human-readable name for a streaming query                                      |
| foreachBatch                              | Treat each micro-batch as a static DataFrame for custom batch logic            |
| Dead Letter Queue (DLQ)                   | Route bad/malformed records aside instead of crashing the whole job            |
| StreamingQueryListener                    | Hook for monitoring/alerting on a streaming query's health                     |
| Stream-Stream Join                        | Joining two live streams — requires watermarks to bound the wait               |
| Auto Loader                               | Databricks incremental file ingestion with schema evolution & backfill support |
