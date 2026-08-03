# Kafka & Streaming — Revision Notes

## 1. What Is Apache Kafka?

**Apache Kafka** is an **open-source, distributed event-streaming platform**. In plain terms: it's a super-fast, reliable "post office" that collects data/events from many different systems in real time, and lets other systems read that data — all at very high speed and scale.

- **Collects/integrates data streams** — pulls events from many different source systems into one central place.
- **Processes real-time event streams** — data flows through continuously, not in one big daily batch.
- **Highly scalable** — can handle huge volumes by spreading work across many machines (brokers).

> Example: An e-commerce site has orders, page-views, and payment events happening every second across different services. Kafka acts as the **central nervous system** collecting all these events, so downstream systems (fraud detection, analytics, recommendation engine) can all consume the same stream independently.

---

## 2. How Kafka Works — The 3 Core Parts

Kafka works on the principle of a **message queue** — producers drop messages in, consumers pick them up.

| Part                 | Role                                                                                                                                                               |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Producer (API)**   | Sends/publishes data (events) **into** the Kafka broker.                                                                                                           |
| **Broker (Cluster)** | The actual Kafka server(s) that **store and manage** the incoming data streams. Multiple brokers together form a **cluster**, for scalability and fault-tolerance. |
| **Consumer (API)**   | Reads/receives data **from** the broker for downstream processing.                                                                                                 |

**A few extra core concepts worth knowing (commonly used alongside these):**
- **Topic** — a named "channel"/category that events are published to (e.g., `orders`, `payments`). Producers write to a topic; consumers read from it.
- **Partition** — each topic is split into partitions, so data can be spread across brokers and read in parallel — this is *how* Kafka scales.
- **Offset** — a unique, ever-increasing ID for each message within a partition, marking its position — consumers track offsets to know what they've already read.
- **Consumer Group** — a set of consumers working together to read a topic, splitting the partitions between them so no two consumers in the group read the same message twice.

> Example use case: A microservices architecture where each service independently reacts to real-time events (e.g., "order placed" event triggers inventory update, billing, and notification services simultaneously) — Kafka decouples these services so they don't call each other directly.

---

## 3. Kafka Setup — Docker Containers

A common local/dev setup runs Kafka using **two Docker containers**:

| Container        | Purpose                                                                                                                                                             | Default Port |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| **ZooKeeper**    | Manages broker metadata — tracks which brokers are alive, cluster configuration, and leader election for partitions. (Traditional/older Kafka setups require this.) | `2181`       |
| **Kafka Broker** | The actual Kafka server that stores and serves the event data.                                                                                                      | `9092`       |

Then an **External Application** (your producer/consumer code) connects to the broker on port `9092` to send/receive events.

> 📌 **Good to know (gap-fill):** Newer versions of Kafka (3.3+) support **KRaft mode**, which **removes the ZooKeeper dependency entirely** — the brokers manage metadata themselves. So if you see a modern Kafka setup with only *one* container type (no ZooKeeper), that's KRaft mode. ZooKeeper + Broker (two containers) is still very common in tutorials and older/legacy deployments though.

---

## 4. Considerations When Designing a Streaming Job

Before building a streaming pipeline, you need to think through **job frequency** — how often it runs, and whether that's "batch-like" (every few minutes) or truly real-time (continuous). This choice creates several challenges to solve for:

- **Each iteration must finish within the frequency window** — if your job is set to run every 2 minutes but takes 5 minutes to process, iterations start piling up/overlapping.
- **Handling data volume** — sudden spikes in incoming data shouldn't break the pipeline.
- **Cleanup & housekeeping** — old files, temp checkpoints, processed data, etc. need to be managed so storage doesn't grow forever.
- **Backpressure** — when data arrives **faster** than it can be processed. The system needs a way to slow down intake or buffer safely instead of crashing/losing data.
- **Scheduling vs. continuous listening** — do you trigger the job on a fixed schedule (e.g., every 5 mins via an orchestrator), or keep a process **always running**, listening for new data as it arrives?
- **Incremental data processing** — only process *new* data each run, not everything from scratch. Key techniques:
  - **Checkpointing** — saving *how far* processing has gotten, so a restart resumes from the right place instead of reprocessing everything (or missing data).
  - **Delta (Lake)** — a storage format/layer that tracks table changes over time, making it easy to read only "what changed" incrementally.
  - **Failure handling** — what happens if a micro-batch fails halfway — can it safely retry without duplicating or losing data?
  - **Late-arriving records** — data that shows up *after* its "expected" time window (e.g., a mobile event delayed by poor network) — pipelines need a strategy (like watermarking) to still handle these correctly instead of ignoring them.

**Orchestration Tool**
A tool that schedules, monitors, and manages the execution of your data jobs/pipelines (handling dependencies, retries, alerting, and timing) — e.g., **Apache Airflow**, **Databricks Workflows**, or **Dagster**. Rather than running your streaming/batch job manually, an orchestrator decides *when* and *in what order* jobs run, and what to do if one fails.

---

## 5. Spark Structured Streaming — Basics

Spark treats a stream as **an ever-growing table** — new data just keeps getting appended, and Spark processes it incrementally.

- **`spark.readStream`** — reads data as a continuous stream (instead of `spark.read` for a one-time static batch read).
- **`.writeStream`** — writes the *processed* stream output somewhere (a table, files, Kafka, etc.), continuously.

### The Micro-Batch Model

Structured Streaming doesn't process record-by-record in true real time by default — it processes in **micro-batches**:

1. The **Streaming Query** continuously watches the source location for new incoming data.
2. As soon as new data lands, the query **updates its checkpoint** and **triggers a micro-batch**.
3. `readStream` reads the new data → your transformations are applied → `writeStream` writes the result out.
4. Once done, the **checkpoint is committed** (marking this data as "processed").
5. The query goes back to **watching for the next batch** of new data, and the cycle repeats.

> Think of it like a mail carrier who checks the mailbox, and *every time* new mail appears, immediately picks it up, processes it, delivers it, then notes down "delivered up to here" before checking the mailbox again.

This gives you **near real-time processing** with the reliability/simplicity of batch processing (each micro-batch is just a small batch job under the hood).

---

## 6. Triggers — Controlling *When* Micro-Batches Run

A **Trigger** tells Spark *how often* to kick off a new micro-batch.

**1. Unspecified (Default)**
A new micro-batch starts **immediately** after the previous one finishes. This is "as fast as possible" processing — the query is always working if there's data to process.

**2. Fixed Interval**
Micro-batches are kicked off at a **user-specified time interval**, regardless of whether the previous batch used the full time or not.
```python
df.writeStream \
  .format("delta") \
  .option("checkpointLocation", "<path>") \
  .trigger(processingTime='2 seconds') \
  .table("<table_name>")
```
Useful when you want predictable, evenly-spaced processing (e.g., every 2 seconds) rather than back-to-back nonstop batches.

**3. Available Now**
A **one-time trigger** that processes **all currently available data** (possibly across multiple micro-batches internally), then **stops on its own** — it does not keep listening for new data afterward.
- Great for **cost savings** — you're not paying for a cluster running 24/7 just to "listen."
- Effectively turns streaming logic into a scheduled **incremental batch** job — you run it periodically (e.g., via an orchestrator) and it only processes what's new since last time, then shuts down.

> Quick comparison: **Unspecified** = "keep going nonstop", **Fixed Interval** = "check in every X seconds", **Available Now** = "process what's here right now, then stop" (like a scheduled catch-up job).

*(Bonus, not in your notes but worth knowing: Spark also has an experimental* **Continuous Processing** *trigger for true low-latency (millisecond-level) processing, as opposed to the micro-batch model — but it has more limitations and is less commonly used in practice.)*

---

## 7. Sources & Sinks

**Source** = where the streaming data comes **from**. **Sink** = where the processed streaming data goes **to**.

| Sources (input)  | Sinks (output)                      |
|------------------|-------------------------------------|
| File/Directory   | File/Directory                      |
| Delta Table      | Delta Table                         |
| Kafka            | Kafka                               |
| Other connectors | `foreach` (custom row-by-row logic) |
|                  | Other connectors                    |

> `foreach` sink is special — it lets you write **custom Python/Scala logic** for handling each row/batch of output yourself (e.g., pushing to a REST API), instead of using a built-in connector.

---

## 8. Cleaning the Source Directory (File-based streams)

When streaming from files in a directory, you can tell Spark to **clean up files after processing** them, so the source folder doesn't grow forever:

```python
.option("cleanSource", "delete")
```
Deletes the source file entirely once it's been processed.

```python
.option("cleanSource", "archive")
.option("sourceArchiveDir", "<path>")
```
Moves the processed file to an **archive directory** instead of deleting it — safer, since you keep a copy for auditing/reprocessing if needed.

---

## 9. Naming a Streaming Query

```python
.queryName("name_of_the_query")
```
Gives your streaming query a **human-readable name**, which makes it much easier to identify in the Spark UI / logs when you're running multiple streaming queries at once (otherwise they just show up as auto-generated IDs).

---

## 10. Idempotence in Streaming

**What is Idempotence?**
An operation is **idempotent** if doing it **once** or doing it **multiple times** produces the **exact same end result**. In streaming, this matters a lot because retries, restarts, and failures are *normal* — not edge cases.

**The Problem Without Idempotence**
Streaming systems almost always guarantee **"at-least-once" delivery** by default (safer to resend than to silently drop data). But that means:
- If a micro-batch fails **after** writing data but **before** the checkpoint is committed, on restart Spark/Kafka will **reprocess that same batch again**.
- Without idempotence, this causes **duplicate records** — e.g., a payment processed twice, an order count inflated, a "user signed up" event counted twice.

> Example: A streaming job writes "Order #123 shipped" to a database. The job crashes right after the write but before checkpointing. On restart, it reprocesses the same event and writes "Order #123 shipped" **again** — now your system thinks it shipped twice.

**How to Achieve Idempotence**

| Technique                                 | How it works                                                                                                                                                                                                                                              |
|-------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Unique keys + Upsert (Merge)**          | Instead of blindly `INSERT`ing, use a unique identifier (e.g., `order_id`, or a combination of `topic+partition+offset`) and do a **merge/upsert**: "insert if new, overwrite if it already exists." Delta Lake's `MERGE INTO` is commonly used for this. |
| **Idempotent Producer (Kafka)**           | Kafka producers can be configured with `enable.idempotence=true` — Kafka then tags each message with a **producer ID + sequence number**, and the broker automatically **drops duplicate sends** caused by producer retries.                              |
| **Deduplication with `dropDuplicates()`** | In Spark, track a unique event ID (often combined with a **watermark**, see below) and drop rows that have already been seen within that time window.                                                                                                     |
| **Idempotent sink design**                | Design the destination system itself to naturally reject/ignore duplicates — e.g., a database with a unique constraint on the event ID, so a duplicate insert simply fails/no-ops instead of creating a second row.                                       |
| **Checkpointing + exactly-once sinks**    | Using sinks that support **transactional/exactly-once writes** (like Delta Lake or Kafka transactions) alongside Spark's checkpointing, so a batch's write and its checkpoint commit happen as a single atomic unit — either both happen or neither does. |

**Pros of Idempotence**
- Safe to **retry** failed batches/messages without corrupting downstream data.
- Enables **exactly-once–like** guarantees on top of an at-least-once delivery system — you get reliability without needing perfect delivery.
- Makes recovering from crashes/restarts much simpler and safer.

**Cons / Trade-offs**
- **Extra overhead** — tracking unique IDs, doing merge/upsert operations, or maintaining dedup state costs more compute and storage than a simple blind append.
- **State management** — deduplication windows need to keep track of "recently seen" IDs, which itself consumes memory/state and needs cleanup (old IDs must eventually expire).
- **Not automatic** — idempotence usually has to be **deliberately designed in** (unique keys, merge logic); it's not something you get for free just by using Kafka or Spark.

---

## 11. Delivery Semantics — At-Most-Once vs At-Least-Once vs Exactly-Once

Closely tied to idempotence — this describes the **guarantee** a streaming system gives about how many times a message is processed:

| Semantic          | Meaning                                                                                         | Risk                                                                                                                                                      |
|-------------------|-------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **At-most-once**  | Each message is processed **0 or 1 times** — never retried.                                     | Risk of **data loss** if a failure happens before processing completes.                                                                                   |
| **At-least-once** | Each message is processed **1 or more times** — retried on failure to guarantee nothing's lost. | Risk of **duplicates** (this is where idempotence becomes essential).                                                                                     |
| **Exactly-once**  | Each message is processed **exactly 1 time**, no matter what failures occur.                    | Hardest to achieve — usually built by combining **at-least-once delivery + idempotent processing/sinks**, rather than being a totally separate mechanism. |

> Good to remember: true "exactly-once" almost never exists as a single built-in guarantee — in practice it's **"at-least-once + idempotence" working together** to *behave* like exactly-once from the outside.

---

## 12. Watermarking (Handling Late Data Properly)

Mentioned earlier as a "late record" problem — here's the actual mechanism Spark uses to solve it:

**Watermark** = a moving threshold that tells Spark: *"I'll wait up to X amount of time for late data, but after that, I'll consider the window closed and stop waiting."*

```python
df.withWatermark("event_time", "10 minutes") \
  .groupBy(window("event_time", "5 minutes")) \
  .count()
```
This says: *"Group events into 5-minute windows, but allow data to arrive up to 10 minutes late before finalizing and dropping a window."*

- Without a watermark, Spark would have to keep **all past state forever**, since a "late" record could theoretically arrive at any time — this isn't sustainable memory-wise.
- With a watermark, old state beyond the threshold is safely **dropped**, keeping memory usage bounded.
- Trade-off: data arriving **later** than the watermark threshold gets **dropped/ignored** — so picking the right watermark duration is a balance between completeness and resource usage.

---

## 13. Output Modes

When writing streaming results, Spark needs to know **how** to write the result table each time it updates — this is the **output mode**:

| Mode         | Meaning                                                           | Typical use                                                                                                |
|--------------|-------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| **Append**   | Only **new rows** since the last trigger are written to the sink. | Simple streaming (e.g., raw events with no aggregation).                                                   |
| **Update**   | Only rows that **changed** since the last trigger are written.    | Aggregations where existing groups can be updated (e.g., running counts).                                  |
| **Complete** | The **entire result table** is re-written every trigger.          | Small aggregation results where you want the full up-to-date picture each time (e.g., a live leaderboard). |

> Not every mode works with every query — e.g., **Append mode** isn't allowed with certain aggregations unless a watermark is defined, since Spark needs to know when a row is truly "final" before appending it.

---

## 14. Schema Evolution & Schema Registry (Kafka-specific, worth knowing)

Real-world event streams change shape over time (new fields added, types changed) — this creates a risk: **consumers break** if a producer suddenly sends data in an unexpected format.

- **Schema Registry** — a separate service (commonly **Confluent Schema Registry**) that stores the *agreed-upon* structure (schema) for each Kafka topic, usually using **Avro**, **Protobuf**, or **JSON Schema**.
- Producers/consumers check against the registry to make sure new data is **compatible** with the existing schema (e.g., you can add optional fields, but can't just remove a required one) before it's allowed to flow through.
- This prevents a schema change on the producer side from silently breaking every downstream consumer.

> Not always needed for small/simple pipelines, but becomes essential once **multiple teams/systems** depend on the same Kafka topic in production.

---

## 15. Stateful vs Stateless Processing

This describes whether a streaming operation needs to **remember anything** about past data to process the current record.

**Stateless Processing**
Each record is handled **independently** — no memory of previous records is needed.
> Example: Filtering out events where `status = "error"`, or converting a temperature field from Celsius to Fahrenheit. Each row is transformed on its own; the result for row #500 doesn't depend on row #499.

- **Implementation:** simple transformations — `filter()`, `select()`, `withColumn()`, `map()`.
- **Pros:** Simple, cheap, scales easily (no shared memory needed across records), fast recovery after failure (nothing to rebuild).
- **Cons:** Limited — can't answer questions like "what's the running total?" or "how many events in the last 5 minutes?"

**Stateful Processing**
The operation needs to **remember information across records/batches** to produce a correct result.
> Example: A running count of orders per customer, a 5-minute rolling average of sensor readings, or detecting "has this user logged in more than 3 times today?"

- **Implementation:** aggregations (`groupBy().count()`, `sum()`), windowed operations, `mapGroupsWithState`/`flatMapGroupsWithState` (for fully custom state logic), stream-stream joins.
- Spark keeps this "state" in a **state store**, backed by the checkpoint location, so it survives restarts.
- **Pros:** Enables real, meaningful analytics (aggregates, trends, patterns) instead of just row-by-row transforms.
- **Cons:**
  - **Grows over time** — state needs cleanup (this is exactly why watermarking exists — to bound state size).
  - **Heavier resource usage** — more memory/storage needed to hold state.
  - **Harder to scale/reshuffle** — changing parallelism (e.g., number of partitions) for a stateful job is trickier since state is tied to specific keys/partitions.
  - Recovery after failure is more involved — the state store itself must be restored, not just "start reading from the last offset."

> Simple way to remember: **Stateless = "each record on its own island."** **Stateful = "records need to talk to their past selves" — which means someone has to remember and store that history.**

---

## 16. Types of Windows

Windows are how streaming systems group events that happen **close together in time** — essential for stateful operations like "count per 5-minute window."

**1. Tumbling Window**
Fixed-size, **non-overlapping**, back-to-back windows. Every event belongs to exactly **one** window.
```python
df.groupBy(window("event_time", "5 minutes")).count()
```
> Example: 12:00–12:05, 12:05–12:10, 12:10–12:15 ... — each 5-min block is separate, no overlap.
- **Pros:** Simple to understand and reason about; each event counted exactly once.
- **Cons:** Can miss patterns that span a window boundary (e.g., a burst of activity from 12:04–12:06 gets split across two windows).
- **Usage:** Regular periodic reporting — e.g., "orders per 5 minutes," hourly aggregates.

**2. Sliding Window**
Fixed-size windows that **overlap**, advancing by a smaller "slide" interval. One event can belong to **multiple** windows.
```python
df.groupBy(window("event_time", "10 minutes", "5 minutes")).count()
```
> Example: A 10-minute window sliding every 5 minutes → windows are 12:00–12:10, 12:05–12:15, 12:10–12:20 ... each overlapping the last.
- **Pros:** Smoother trend detection — avoids the "hard cutoff" problem of tumbling windows; good for moving averages.
- **Cons:** More compute/state overhead since each event is counted in multiple windows at once.
- **Usage:** Moving averages, smoothing out noisy metrics (e.g., "average CPU load over the last 10 mins, updated every minute").

**3. Session Window**
**Dynamic-length** window based on actual **activity gaps**, rather than a fixed clock — a window stays "open" as long as new events keep arriving within a gap threshold, and "closes" once that gap of inactivity passes.
```python
df.groupBy(session_window("event_time", "10 minutes")).count()
```
> Example: A user browsing a website — their "session" stays open as long as they click something at least every 10 minutes; if they go quiet for 10+ minutes, the session closes, and their next click starts a brand-new session.
- **Pros:** Naturally maps to real user/device behavior (session length isn't fixed/arbitrary).
- **Cons:** Less predictable — window size varies, which can complicate downstream processing and makes state size harder to bound.
- **Usage:** User session analytics, clickstream analysis, IoT device "active periods."

> Quick comparison: **Tumbling** = fixed, no overlap, simplest. **Sliding** = fixed, overlapping, smoother trends. **Session** = variable length, driven by actual activity gaps.

---

## 17. Checkpointing — Deep Dive

Checkpointing was mentioned earlier as a general concept — here's what it actually does and stores under the hood, since it's central to almost everything above (recovery, state, exactly-once-like behavior).

**How it works**
On every micro-batch, Spark writes the following to the checkpoint location (a durable path, e.g., on cloud storage):
- **Offsets/progress** — exactly which data (e.g., which Kafka offsets, or which files) has been read and processed so far.
- **State store snapshots** — for stateful operations, the actual aggregation/state data (e.g., running counts, join buffers) needed to resume correctly.
- **Metadata about the query itself** — configuration used, so a restart uses consistent settings.

On restart/failure recovery, Spark reads this checkpoint and **resumes exactly where it left off** — instead of reprocessing everything from scratch or skipping unprocessed data.

**Pros**
- Enables **fault tolerance** — a crashed streaming job can restart and pick up correctly.
- Enables **stateful processing** to survive restarts (without it, all aggregation state would be lost on failure).
- Combined with idempotent sinks, gets you close to **exactly-once** behavior.

**Cons / Trade-offs**
- **Storage overhead** — checkpoints (especially state store snapshots) consume real disk/cloud storage, which grows with state size.
- **Can't casually change your query logic** — significantly altering the transformation logic (e.g., changing aggregation keys) after a checkpoint exists can break compatibility, sometimes forcing you to start a fresh checkpoint (losing continuity).
- **Slight performance cost** — writing checkpoint data on every micro-batch adds overhead vs. not persisting anything.
- Checkpoint location **must be reliable, durable storage** — losing the checkpoint directory means losing the ability to recover state/progress cleanly.

> Rule of thumb: **never delete or move a checkpoint directory** for a running production streaming job unless you deliberately intend to reset it and reprocess from scratch.

---

## 18. A Few Other Topics Worth Knowing (Suggested Additions)

A handful of concepts that naturally extend what's above, worth being aware of even briefly:

- **Stream-Stream & Stream-Static Joins** — joining two live streams together (e.g., matching "ad clicks" with "ad impressions") is much harder than a normal join, since Spark has to decide *how long* to wait for a matching record on the other side — this is exactly where watermarks become required, not just optional.
- **Kafka Replication & ISR (In-Sync Replicas)** — each Kafka partition is replicated across multiple brokers for durability; the **ISR** is the set of replicas fully caught up with the leader. This is *how* Kafka avoids data loss if a broker dies.
- **Consumer Lag** — the gap between the latest offset in a partition and the offset a consumer has actually processed. Monitoring this tells you if your consumers are **falling behind** the incoming data rate — a key operational health metric for any streaming pipeline.
- **Compaction (Kafka log compaction)** — an alternative retention strategy where Kafka keeps only the **latest value per key** instead of deleting old messages after a time period — useful for topics that represent "current state" (e.g., "latest known address per customer_id") rather than an event history.

---

## 19. Late-Arriving Data — Handling It Properly

This was touched on with watermarking, but it deserves its own breakdown since it's a very common real-world headache.

**Why does data arrive late?**
- A mobile device was offline and syncs hours later.
- Network delays or retries in an upstream system.
- A batch source only delivers data at the end of the day, covering events from earlier.

**The core problem**
Once you've closed a window and emitted a result (say, "5-minute order count = 42"), what happens if 3 more orders for that same window show up 20 minutes later? Do you:
- (a) Ignore them (simplest, but your numbers are now **wrong/incomplete**), or
- (b) Update the earlier result (more correct, but requires the sink to support **updates**, not just blind appends)?

**How it's handled**

| Approach                                          | How it works                                                                                                                                                                           | Trade-off                                                                                                         |
|---------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| **Watermarking**                                  | Define how long you'll tolerate lateness (e.g., "10 minutes"); Spark keeps the window state open that long, then finalizes and drops it.                                               | Simple, bounded memory — but anything later than the threshold is **dropped**.                                    |
| **`Update` output mode**                          | Instead of `Append`, use `Update` mode so that if a late record updates an existing window's aggregate, the sink receives a **corrected value** rather than a brand-new duplicate row. | Requires a sink that can handle updates/upserts (e.g., a database key, or Delta `MERGE`), not a simple flat file. |
| **Wider watermark / buffer window**               | Increase the lateness tolerance (e.g., 1 hour instead of 10 minutes) if your data is known to be late fairly often.                                                                    | More accurate, but **more state kept in memory longer** — costs more resources.                                   |
| **Dead-letter / side-output for "too-late" data** | Instead of silently dropping records past the watermark, route them to a **separate location** (a "late arrivals" table) for manual review or a separate reconciliation job.           | Extra pipeline complexity, but nothing is silently lost — you can inspect/reprocess it later.                     |

> Example: An IoT sensor pipeline sets a 10-minute watermark. A sensor goes offline and reconnects 30 minutes later, dumping its backlog. Those readings are now **past the watermark** and get dropped by default — unless you've set up a dead-letter path to catch and reprocess them separately.

**Key trade-off to remember:** there is no free lunch here — the choice is always between **(1)** dropping some late data to keep things simple and bounded, or **(2)** accepting extra complexity/state/cost to capture it more completely.

---

## 20. Backfilling — Reprocessing Historical Data

**What is backfilling?**
Running a pipeline over **past data** that was either never processed, or needs to be **reprocessed** — as opposed to normal streaming, which only handles new incoming data.

**Common reasons you need to backfill**
- A **bug** in your transformation logic is fixed, and historical output needs correcting.
- A **new feature/column** is added to the pipeline, and you want it applied to historical data too, not just data going forward.
- **Initial load** — bringing a brand-new streaming pipeline up to date with everything that already existed before it started.
- **Late-arriving data** past the watermark needs a separate catch-up run (see above).

**How backfilling is typically done**

- **`Trigger.AvailableNow`** — point the job at the historical data location and let it process everything currently available, then stop. This is the most common Spark Structured Streaming approach to backfilling, since it reuses your existing streaming logic rather than writing separate batch code.
- **Separate checkpoint location** — critical detail: a backfill job should usually use **its own checkpoint path**, different from your live/production streaming job's checkpoint. Reusing the same checkpoint can confuse offset tracking between the "catch-up" run and the "live" run.
- **Kafka offset reset** — to reprocess historical Kafka data, you set the consumer to start from an earlier point using `startingOffsets` (e.g., `"earliest"` or a specific offset/timestamp) instead of `"latest"`.
- **Delta Lake time travel** — Delta lets you query a table **as of a previous version or timestamp** (`VERSION AS OF`, `TIMESTAMP AS OF`), which is handy for backfilling from a known historical snapshot.
- **Date-range partitioned reprocessing** — if your data is partitioned by date, you can backfill by simply pointing a batch/stream job at the specific date-range folders that need reprocessing.

**Issues to watch out for**

- **Duplicates** — since backfill data overlaps with what may have already been processed live, this is exactly where **idempotent writes** (upsert/merge, unique keys) become essential — otherwise you double-count everything you backfill.
- **Resource spikes** — processing months of historical data at once can be far heavier than your usual micro-batch size; may need a bigger cluster temporarily, or chunking the backfill into smaller date ranges.
- **Ordering/consistency** — if the live pipeline is running *at the same time* as a backfill, make sure they don't both try to write to overlapping time ranges simultaneously, causing conflicting updates.
- **Schema mismatches** — old historical data may not match your *current* schema (missing columns, different types) — needs handling (defaults, casting) before it fits into today's pipeline logic.
- **Cost** — reprocessing large volumes of historical data isn't free — plan and budget for it rather than triggering it casually.

> Simple way to remember: **backfilling = replaying the past through (mostly) the same pipeline** — but it needs its *own* checkpoint, careful offset/version selection, and idempotent writes so it doesn't corrupt or duplicate what's already live.

---

## 21. A Few More Concepts Worth Adding

Some additional gaps worth filling in, since they come up constantly alongside everything above:

**Rate Limiting (a direct answer to "backpressure")**
Earlier notes mention backpressure as a problem — here's how it's actually controlled in Spark:
- `maxOffsetsPerTrigger` (Kafka source) — caps how many Kafka messages get pulled into a single micro-batch.
- `maxFilesPerTrigger` / `maxBytesPerTrigger` (file source) — caps how many new files (or how much data) get picked up per micro-batch.
> Example: If a huge backlog of files suddenly appears, setting `maxFilesPerTrigger=100` processes them **gradually**, 100 files at a time per batch, instead of one massive batch trying to swallow everything at once and running out of memory.

**Handling Malformed / "Poison Pill" Records**
Real streams eventually get a record that breaks your parsing/transformation logic (bad JSON, unexpected type, corrupt bytes). If unhandled, this can **crash the entire streaming query**.
- **`badRecordsPath`** (or the `PERMISSIVE`/`DROPMALFORMED`/`FAILFAST` parse modes) — lets Spark route unparseable records to a separate location instead of failing the whole job.
- **Dead-letter queue (DLQ) pattern** — in `foreachBatch`, wrap your logic in error handling so a bad record gets written to a separate "quarantine" table/topic for later inspection, while good records keep flowing normally.

**`foreachBatch`**
A very commonly used sink that gives you a plain **batch DataFrame** for each micro-batch, letting you run *any* normal batch logic (multiple writes, `MERGE INTO`, custom error handling, writing to multiple destinations) — often the practical glue that ties together idempotent writes, DLQ handling, and backfill logic in one place.

**Auto Loader (Databricks-specific, but very relevant to backfilling)**
A Databricks feature (`cloudFiles` source) built specifically for **incrementally and efficiently ingesting new files** from cloud storage, with:
- Automatic **schema inference & evolution** — adapts as new columns show up over time.
- Efficient file discovery — avoids expensive full-directory listing on every batch, even at huge scale.
- Native support for **backfilling**, via a `backfillInterval` option that periodically re-scans in case some files were missed by the normal incremental listing.

---

## 19. Late-Arriving Data — Issues & How to Handle It

This deserves its own deep-dive since it trips up a lot of real pipelines.

**Why data arrives "late"**
- **Event time vs. Processing time** — event time is *when something actually happened* (e.g., a sensor reading at 12:00:00); processing time is *when your system actually sees it* (e.g., 12:07:00, because of a network delay). Late data = event time is much earlier than processing time.
- Common causes: mobile/IoT devices going offline and syncing later, network delays, upstream system retries/backpressure, clock skew between systems.

**The Problem Without Handling It**
- If you finalize a 5-minute window and emit results, then a late record for that same window shows up 10 minutes later — do you **ignore it** (inaccurate result) or **update the already-emitted result** (requires re-triggering downstream systems)?
- Without any lateness limit, Spark would have to **keep all historical state forever**, "just in case" an old record shows up — this makes memory/state grow unbounded and eventually crashes the job.

**How It's Handled — Watermarking (recap + more detail)**
```python
df.withWatermark("event_time", "10 minutes") \
  .groupBy(window("event_time", "5 minutes")) \
  .count()
```
This tells Spark: *"track the max event time seen so far; once event time has advanced 10 minutes past a window's end, close that window and drop its state."*
- Data arriving **within** the watermark threshold → correctly included, updates the result.
- Data arriving **later than** the watermark threshold → silently **dropped** (in most cases) since Spark has already discarded the state for that window.

**Choosing the Watermark Duration — a Real Trade-off**
| Watermark | Effect |
|---|---|
| Too **short** | More late data gets dropped/lost → less accurate results, but low memory usage and low latency (results finalize quickly). |
| Too **long** | Captures more late data → more accurate, but **higher memory/state usage** and results take longer to finalize (higher latency before a window is "done"). |

**Output Mode Matters Here**
- **Append mode** — a row is only written once its window is *finalized* (i.e., after the watermark passes) — so genuinely late data (data that arrives even later) simply can't be added afterward.
- **Update mode** — allows a window's result to be **revised** as late (but still within-watermark) data trickles in, before final close — better accuracy for slightly-delayed data, at the cost of downstream systems needing to handle "updates" to previously-seen results, not just new rows.

> Practical tip: if your source is known to have delays up to, say, 15 minutes (e.g., mobile app syncing), set the watermark a bit *above* that (e.g., 20 minutes) rather than guessing low — dropped late data is often a silent, hard-to-debug data quality issue.

---

## 20. Backfilling — Reprocessing Historical/Missed Data

**What is Backfilling?**
Re-running processing over **historical data** — either because:
- A pipeline was down for a while and missed a chunk of data (**gap-filling**), or
- The transformation logic changed, and you need to **reprocess old data** with the new logic.

**Why Backfilling Is Tricky in Streaming**
- **Duplicate risk** — if backfilled data overlaps with what the live stream already processed, you can easily end up double-counting unless writes are idempotent (merge/upsert, unique keys).
- **Watermark conflicts** — if you feed old (backfill) data into the *same* live streaming query, the watermark has likely already advanced far ahead (based on live/current event times) — so the old backfill data may get **immediately treated as "too late" and dropped**, since it looks late relative to the current watermark.
- **Resource spikes** — a backfill often means processing a much larger volume of data at once than a normal micro-batch expects, which can overwhelm cluster resources if not throttled.
- **Ordering matters for stateful jobs** — if your logic depends on chronological order (e.g., running totals), replaying backfill data out of order relative to live data can produce incorrect results.

**Recommended Ways to Handle Backfilling**
1. **Run backfill as a separate batch job, not inside the live stream.** Use `spark.read` (regular batch, not `readStream`) over the historical date range, apply the *same* transformation logic, and write using an **idempotent merge/upsert** into the destination table — so it safely coexists with whatever the live stream already wrote.
2. **Use `Trigger.AvailableNow`** for a one-off catch-up run when you just need to process "everything that piled up" once, then stop — cleaner than trying to force it through a continuous stream.
3. **Replay from Kafka using offsets/timestamps** — Kafka lets a consumer **seek to a specific offset or timestamp** (e.g., "start reading from 3 days ago") to intentionally re-consume historical events for backfill purposes (as long as retention hasn't expired those messages).
4. **Write to a separate table/version first, then merge** — safer than writing backfill data directly into a live production table; validate correctness, then merge it in.
5. **Always pair with idempotent sinks** (see §10) — this is what actually makes it *safe* to backfill without creating duplicates, regardless of which method above you use.

> Rule of thumb: **treat backfilling as a batch problem, not a streaming problem** — borrow your streaming job's transformation logic, but run it as a one-time/scheduled batch job with careful deduplication, rather than trying to "inject" old data into a live, continuously-running stream.

---

## 21. A Few More Important Concepts (Additional Gaps Worth Knowing)

- **Dead Letter Queue (DLQ) / Error Handling** — real-world streams always contain some malformed/unexpected records (bad JSON, missing fields, wrong types). Instead of letting one bad record **crash the whole streaming job**, a common pattern is to catch the error and route the bad record to a separate "dead letter" topic/table for later inspection, while letting good records continue flowing normally.
  > Example: A record with an unparseable timestamp gets written to a `bad_records` table instead of stopping the entire pipeline for everyone else's valid data.

- **`foreachBatch`** — lets you treat each micro-batch as a regular (static) DataFrame and run **arbitrary batch logic** on it — e.g., writing to multiple sinks, doing a custom merge/upsert, or running deduplication logic that isn't natively supported as a streaming sink. Very commonly used together with backfilling/idempotent merge patterns above.
  ```python
  def write_batch(batch_df, batch_id):
      batch_df.write.format("delta").mode("append").save("<path>")

  df.writeStream.foreachBatch(write_batch).start()
  ```

- **Monitoring Streaming Queries** — production pipelines need visibility into health, not just "is it running." Key things to watch:
  - **Input rate vs. processing rate** — if input consistently outpaces processing, you have a backpressure problem building up.
  - **Batch duration** — sudden spikes suggest resource issues or a skewed/oversized batch.
  - **`StreamingQueryListener`** — a Spark API to hook into query start/progress/termination events for custom alerting/logging (e.g., send a Slack alert if a query stops unexpectedly).

- **Ordering Guarantees in Kafka** — Kafka only guarantees message order **within a single partition**, not across an entire topic. If strict ordering matters for a given entity (e.g., all events for one `customer_id` must be processed in order), you need to ensure they're always sent to the **same partition** (typically by using that ID as the message key, since Kafka partitions by key hash).

---

### Quick Recap Table

| Term                          | One-liner                                                                                |
|-------------------------------|------------------------------------------------------------------------------------------|
| Kafka                         | Distributed platform for collecting & processing real-time event streams                 |
| Producer / Broker / Consumer  | Sends data → stores/manages data → reads data                                            |
| Topic / Partition / Offset    | Channel → parallel split of channel → position marker within it                          |
| ZooKeeper                     | Manages broker metadata (older Kafka setups; replaced by KRaft in newer ones)            |
| Backpressure                  | Data arriving faster than it can be processed                                            |
| Checkpointing                 | Saving processing progress so restarts resume correctly                                  |
| Micro-batch                   | Spark's model: watch → trigger → process → commit checkpoint → repeat                    |
| Trigger: Unspecified          | Run next batch immediately after previous finishes                                       |
| Trigger: Fixed Interval       | Run batches at a set time interval                                                       |
| Trigger: Available Now        | Process all current data once, then stop (cost-efficient)                                |
| Source / Sink                 | Where streaming data comes from / goes to                                                |
| cleanSource                   | Auto-delete or archive files after they're processed                                     |
| queryName                     | Human-readable name for a streaming query                                                |
| Idempotence                   | Same operation run multiple times = same end result (no duplicates)                      |
| At-least/most/exactly-once    | Delivery guarantees on how many times a message gets processed                           |
| Watermark                     | Threshold for how long to wait for late data before closing a window                     |
| Output Modes                  | Append (new rows only) / Update (changed rows) / Complete (full table)                   |
| Schema Registry               | Central store enforcing compatible schemas across producers/consumers                    |
| Stateless Processing          | Each record handled independently, no memory needed                                      |
| Stateful Processing           | Operation needs memory of past records (aggregates, joins, windows)                      |
| Tumbling Window               | Fixed, non-overlapping time windows                                                      |
| Sliding Window                | Fixed, overlapping windows advancing by a slide interval                                 |
| Session Window                | Variable-length window based on activity gaps, not the clock                             |
| Checkpointing (deep dive)     | Stores offsets + state snapshots so a job resumes exactly where it left off              |
| Consumer Lag                  | How far behind a consumer is from the latest data — key health metric                    |
| Kafka ISR                     | In-sync replicas — brokers fully caught up, used for durability                          |
| Event Time vs Processing Time | When something happened vs. when your system actually saw it                             |
| Late Data                     | Event time much earlier than processing time — handled via watermarking                  |
| Backfilling                   | Reprocessing historical/missed data — best done as an idempotent batch job               |
| Dead Letter Queue (DLQ)       | Route bad/malformed records aside instead of crashing the whole job                      |
| foreachBatch                  | Treat each micro-batch as a static DataFrame for custom batch logic                      |
| StreamingQueryListener        | Hook for monitoring/alerting on a streaming query's health                               |
| Kafka Ordering                | Guaranteed only within a single partition, not across a whole topic                      |
| Late Data Handling            | Watermark / Update mode / wider buffer / dead-letter path for late records               |
| Backfilling                   | Reprocessing historical data — own checkpoint, offset/version control, idempotent writes |
| Rate Limiting                 | `maxOffsetsPerTrigger` / `maxFilesPerTrigger` — directly controls backpressure           |
| Poison Pill / DLQ             | Routing bad/unparseable records to a quarantine location instead of crashing the job     |
| foreachBatch                  | Access each micro-batch as a normal DataFrame for custom batch-style logic               |
| Auto Loader                   | Databricks incremental file ingestion with schema evolution & backfill support           |

