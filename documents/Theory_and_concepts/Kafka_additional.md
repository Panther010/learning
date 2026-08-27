# Kafka — Theory & CLI Reference Notes

---

## 1. What Is Kafka?

**Kafka** is a **distributed messaging system**, originally created by **LinkedIn**. It provides **fast, highly scalable, and redundant messaging** through a **publish-subscribe (pub-sub) model**.

Because of its distributed design, Kafka offers:
- Support for a **large number of permanent or ad-hoc consumers** reading the same data.
- **High availability** — resilient to node failures, with **automatic recovery**.
- Being **distributed, resilient, and fault-tolerant** by design — no single point of failure if configured correctly.

---

## 2. Core Terminology

| Term | Meaning |
|---|---|
| **Topic** | All Kafka messages are organized into topics — a named category/stream of data. |
| **Producer** | Pushes (writes) messages **into** a Kafka topic. |
| **Consumer** | Pulls (reads) messages **off** a Kafka topic. |
| **Broker** | Kafka runs as a cluster; each **node** in that cluster is called a broker. |

---

## 3. Topics — In Depth

- A topic is a **stream of data** — conceptually similar to a **table** in a database.
- Identified by its **name**.
- A topic is divided into a number of **partitions**, which allow the topic to be **parallelized** by splitting the data across them.
- Each message within a partition has a unique identifier called its **offset**.
- The offset defines the **ordering of messages as an immutable sequence** — Kafka guarantees this order is maintained.
- Consumers can start reading from **any offset** they choose, letting them join the stream at whatever point makes sense for them.
- **Every message is uniquely identified** by the tuple: **(topic, partition, offset)**.
- **Order is only guaranteed within a partition — never across partitions of the same topic.**
- **Retention** — data is kept for a limited time (**default: 1 week**), not forever, unless configured otherwise (see log compaction/retention settings).
- **Immutability** — once written to a partition, a message **cannot be changed**.
- **Partition assignment** — if no key is provided, messages are assigned to a partition **randomly** (technically round-robin); if a key **is** provided, Kafka uses hashing to consistently route same-key messages to the same partition (see Producers, §5).

---

## 4. Partitions & Brokers

- A Kafka **cluster** is composed of multiple **brokers**.
- Each broker is identified by an **integer ID**.
- Each broker holds a subset of partitions — Kafka **randomly distributes** partitions across the available brokers.
- **You only need to connect to one broker to be effectively connected to the entire cluster** (see Broker Discovery, §8).
- For a given topic, each partition has:
  - One **leader** replica.
  - Zero or more **follower/replica** copies (also called **ISR** — In-Sync Replicas, once caught up).
- **All reads and writes** for a partition go through its **leader**; the leader is responsible for propagating new data to its replicas.
- If a leader broker fails, one of its **in-sync replicas is promoted** to become the new leader automatically.
- A topic should be configured with a **replication factor greater than 1** for durability — partitions of a topic get replicated across multiple brokers, so losing one broker doesn't lose data.

> **Kafka property to remember:** with a replication factor of **N**, Kafka can tolerate **N−1** broker failures without losing data.

---

## 5. Producers

- Producers **write data to partitions**.
- The producer itself **decides** which partition/broker a given message is written to.
- If a broker fails, the producer **automatically recovers** and adjusts.
- Producers naturally handle **load balancing** by spreading data across different brokers.

**Acknowledgment (`acks`) Levels**
Producers can choose how much confirmation they wait for before considering a write "successful":

| Setting | Behavior | Risk |
|---|---|---|
| **`acks=0`** | Producer does **not wait** for any acknowledgment at all. | Fastest, but **highest risk of data loss**. |
| **`acks=1`** | Producer waits for an ack from the **leader** only. | Balanced — safe from leader-level issues, but a leader crash right after ack (before replication) can still lose data. |
| **`acks=all`** | Producer waits for acks from **all in-sync replicas**. | Slowest, but **safest** — very low risk of data loss. |

**Keyed vs. Non-Keyed Messages**
- A producer can optionally send data with a **key** (string or number).
- **If the key is `null`** → data is distributed to brokers/partitions in a **round-robin** manner.
- **If a key is provided** → messages with the **same key always go to the same partition**, thanks to a **hashing** mechanism mapping key → partition.
> Example: Using `customer_id` as the key ensures all events for one customer land in the same partition, preserving their relative order.

---

## 6. Consumers

- Consumers **read data from a topic**.
- A consumer automatically knows which broker to read from, and how to **recover** in case of failure.
- Data is read **in order within each partition** — but there's **no ordering guarantee across partitions**.
- A consumer is simply an application (written in any supported language) that reads data from a topic.

**Consumer Groups**
- Consumers read data as part of a **consumer group**.
- Multiple consumers can run at the same time within a group, each reading from **different partitions**.
- **If there are more consumers than partitions** → the extra consumers sit **idle** (inactive), since a partition can only be read by one consumer in a group at a time.
- **If there are fewer consumers than partitions** → some consumers will read from **more than one partition**.
- If a consumer in the group dies, Kafka **automatically redistributes** its partitions among the remaining consumers (a "rebalance").

---

## 7. Consumer Offsets & Delivery Guarantees

- Kafka tracks the **offset** at which a consumer group has been reading — essentially a **checkpoint** of consumption progress.
- These offsets are stored (committed) in a special **internal Kafka topic** called `__consumer_offsets`.
- After processing a message, the consumer **commits** its offset — this is what allows processing to **resume correctly** if a consumer restarts or crashes mid-processing.
- **The consumer decides when to commit** the offset — and this choice defines the delivery guarantee:

| Strategy | How it works | Trade-off |
|---|---|---|
| **At-Most-Once** | Offset is committed **as soon as the message is received** (before processing). | Fastest, but data can be **lost** if processing fails after the commit. |
| **At-Least-Once** | Offset is committed **only after** the message is fully processed. | If a failure happens, the message is **re-read** — safer, but can create **duplicates**. Use when duplicates don't harm your application. |
| **Exactly-Once** | Only truly achievable for **Kafka-to-Kafka** processing (via Kafka transactions). For external systems, you need to design an **idempotent consumer** to effectively achieve the same result. |

---

## 8. Kafka Broker Discovery

Every Kafka server acts as a **bootstrap server** — meaning any single broker you connect to can tell you how to reach every other broker in the cluster.

- Every broker knows about **all other brokers**, **all topics**, and **each partition's location** — i.e., every broker holds the full cluster **metadata**.
- This is how a client can connect to just **one** broker and still access data that actually lives on a different broker:
  1. Client connects to any one broker and **requests metadata**.
  2. That broker responds with metadata, including the **full list of brokers**.
  3. From this metadata, the client figures out **which broker actually holds** the required partition/data.
  4. The client then connects **directly** to that broker to fetch the data.
- This discovery mechanism is **already built into the Kafka client libraries** — you don't need to implement it yourself.

---

## 9. ZooKeeper's Role (Traditional Kafka Architecture)

- **ZooKeeper** manages the brokers and **holds the cluster together**.
- It handles **leader election** among brokers/replicas.
- It **notifies Kafka** whenever a relevant change happens in the cluster (e.g., a broker going down).
- In traditional (pre-KRaft) Kafka, **Kafka cannot function without ZooKeeper**.
- ZooKeeper itself is designed to run with an **odd number of servers** (for proper quorum/majority voting during elections).
- ZooKeeper follows a **leader-follower model** internally: **writes go to the leader**, while **followers can serve reads**.

> 📌 Note: Newer Kafka versions (3.3+) support **KRaft mode**, which removes the ZooKeeper dependency entirely — brokers manage this metadata/coordination themselves instead.

---

## 10. Key Kafka Properties (Summary)

- Messages are **appended to a topic partition in the order they are sent**.
- Consumers **read messages in the order they were stored** (within a partition).
- With a replication factor of **N**, Kafka can tolerate **N−1** broker failures.
- As long as the **number of partitions stays unchanged**, the **same key will always map to the same partition** (since the hash-to-partition mapping depends on partition count).

---

# Part 2 — CLI Reference

*(Consolidated from your notes — duplicate/near-duplicate command blocks merged into one clean reference.)*

## 11. Starting ZooKeeper & Kafka (local/Windows example)

```bash
# Start ZooKeeper
zookeeper-server-start.bat config\zookeeper.properties

# Start Kafka broker
kafka-server-start.bat config\server.properties
```
*(On Linux/Mac, drop the `.bat` and use the `.sh` scripts instead, e.g. `zookeeper-server-start.sh`.)*

---

## 12. Topic Commands

```bash
# Create a topic
kafka-topics --zookeeper 127.0.0.1:2181 --topic first_topic --create \
  --partitions 3 --replication-factor 1

# List all topics
kafka-topics --zookeeper 127.0.0.1:2181 --list

# Describe a topic (partitions, replicas, leader info, etc.)
kafka-topics --zookeeper 127.0.0.1:2181 --topic testLogs --describe

# Delete a topic
kafka-topics --zookeeper 127.0.0.1:2181 --topic testLogs --delete
```
> Note: some Kafka versions/distributions use `./kafka-topics.sh` with the same flags — the underlying options (`--create`, `--list`, `--describe`, `--delete`) work the same either way.

---

## 13. Producer Commands

```bash
# Basic producer (type messages interactively after running)
kafka-console-producer --broker-list 127.0.0.1:9092 --topic first_topic

# Producer that waits for acknowledgment from ALL in-sync replicas
kafka-console-producer --broker-list 127.0.0.1:9092 --topic first_topic \
  --producer-property acks=all

# Producer sending KEY,VALUE pairs (parse.key enables key parsing)
kafka-console-producer --broker-list 127.0.0.1:9092 --topic first_topic \
  --property parse.key=true --property key.separator=,
> key,value
> another key,another value
```
> 📌 If you produce to a topic that doesn't exist yet, Kafka shows a warning and **auto-creates** the topic with default settings (configurable via `config/server.properties`).

---

## 14. Consumer Commands

```bash
# Basic consumer, reading only NEW messages from now on
kafka-console-consumer --bootstrap-server 127.0.0.1:9092 --topic first_topic

# Consumer reading ALL messages from the beginning of the topic
kafka-console-consumer --bootstrap-server 127.0.0.1:9092 --topic first_topic --from-beginning

# Consumer reading and printing KEYS alongside values
kafka-console-consumer --bootstrap-server 127.0.0.1:9092 --topic first_topic \
  --from-beginning --property print.key=true --property key.separator=,

# Consumer as part of a named consumer group
kafka-console-consumer --bootstrap-server 127.0.0.1:9092 --topic first_topic \
  --group my-first-application
```

**Multiple Consumers in One Group**
Running the **same** `--group` command multiple times (in separate terminals) opens multiple consumers in the **same group**. Kafka automatically divides the topic's partitions among them.
> Example: 3 partitions + 3 consumers in the same group → each consumer gets exactly one partition's messages. If a consumer drops out, Kafka **redistributes** its partition(s) to the remaining consumers.

Kafka tracks offsets **per consumer group** — once a group has read up to a certain point, restarting that group will resume from **new messages only** (unless you explicitly reset the offset — see below).

---

## 15. Consumer Group Commands

```bash
# List all consumer groups
kafka-consumer-groups --bootstrap-server localhost:9092 --list

# Describe a specific group (see below for what this shows)
kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group my-first-application
```

**What `--describe` shows you:**
- The list of topics/partitions the group is (or was) consuming.
- **Current offset** — where this consumer group's reading currently stands.
- **Log-end offset** — the very last offset available on the producer side (i.e., "latest").
- **Lag** — the difference between log-end offset and current offset, per partition (how far behind the consumer is).
- **Active consumer ID(s)**, if the group currently has active members.

**Resetting Consumer Group Offsets**
```bash
# Reset to the earliest available offset (replay everything)
kafka-consumer-groups --bootstrap-server localhost:9092 --group my-first-application \
  --reset-offset --to-earliest --execute --all-topics

# Reset to earliest, for one specific topic only
kafka-consumer-groups --bootstrap-server localhost:9092 --group my-first-application \
  --reset-offset --to-earliest --execute --topic first-topic

# Shift the offset forward by 2 (skip ahead)
kafka-consumer-groups --bootstrap-server localhost:9092 --group my-first-application \
  --reset-offset --shift-by 2 --execute --topic first-topic

# Shift the offset backward by 2 (re-read the last 2 messages)
kafka-consumer-groups --bootstrap-server localhost:9092 --group my-first-application \
  --reset-offset --shift-by -2 --execute --topic first-topic
```
> ⚠️ A consumer group must typically be **inactive** (no running consumers) for an offset reset to apply cleanly.

---

## Quick Recap Table

| Term | One-liner |
|---|---|
| Topic | Named stream of data, like a table; split into partitions |
| Partition | Sub-division of a topic enabling parallelism; order guaranteed only within it |
| Offset | Unique, ordered position of a message within a partition |
| Broker | A single Kafka server/node in the cluster |
| Leader / ISR | Partition owner handling reads/writes / replicas fully caught up |
| Replication Factor N | Tolerates up to N−1 broker failures |
| acks=0/1/all | No wait / leader-only wait / full replica wait — speed vs. safety trade-off |
| Keyed message | Same key → always same partition, via hashing |
| Consumer Group | Set of consumers splitting a topic's partitions between them |
| Rebalance | Automatic partition redistribution when a consumer joins/leaves a group |
| __consumer_offsets | Internal topic storing each group's committed offsets |
| At-most/least/exactly-once | Commit-before vs. commit-after processing vs. transactional guarantee |
| Bootstrap Server | Any broker — used to discover the full cluster's metadata |
| ZooKeeper | Manages brokers, leader election, and cluster change notifications (pre-KRaft) |
| `kafka-topics` | CLI for creating/listing/describing/deleting topics |
| `kafka-console-producer` | CLI for sending test messages to a topic |
| `kafka-console-consumer` | CLI for reading messages from a topic |
| `kafka-consumer-groups` | CLI for inspecting/resetting consumer group offsets |

