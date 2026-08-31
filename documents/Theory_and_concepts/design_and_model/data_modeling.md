# Data Modeling — Revision Notes
*(Organized basic → advanced: what modeling is → building blocks → normalization → OLTP/OLAP & dimensional modeling → modern approaches)*

---

# PART 1 — Fundamentals

## 1. What Is Data Modeling?

**Data Modeling** is the process of designing **how data is organized, stored, and related** in a system — essentially, creating a "blueprint" for your data before you actually build the database.

> Think of it like an architect's blueprint for a house: you plan out the rooms (tables), how they connect (relationships), and what goes in each room (columns/attributes) — **before** pouring the concrete (creating actual tables).

**Why it matters:** a poorly modeled database leads to duplicate/inconsistent data, slow queries, and a system that's painful to change later. Good modeling upfront saves huge pain down the line.

---

## 2. The Three Levels of Data Models

Data modeling is usually done in **three progressively detailed stages**:

| Level                | What it captures                                                                                                                                                          | Example                                                                          |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| **Conceptual Model** | The **big picture** — what entities exist and how they relate, with **no technical detail** (no data types, no keys). For business stakeholders.                          | "A Customer places an Order. An Order contains Products."                        |
| **Logical Model**    | Adds structure — **attributes, data types, keys, relationships** — but still **independent of any specific database technology**.                                         | `Customer(customer_id, name, email)`, `Order(order_id, customer_id, order_date)` |
| **Physical Model**   | The **actual implementation** — specific to your database system (e.g., PostgreSQL, Snowflake), including exact column types, indexes, partitioning, and storage details. | `CREATE TABLE customer (customer_id BIGINT PRIMARY KEY, ...)`                    |

> Simple way to remember: **Conceptual = "what"**, **Logical = "how it's structured"**, **Physical = "how it's actually built."**

---

## 3. Entities, Attributes & Relationships (ER Modeling)

The classic starting point for modeling — **Entity-Relationship (ER) modeling**.

- **Entity** — a real-world "thing" you want to store data about (e.g., `Customer`, `Product`, `Order`). Becomes a **table**.
- **Attribute** — a property/characteristic of an entity (e.g., a Customer has a `name`, `email`, `phone`). Becomes a **column**.
- **Relationship** — how two entities are connected (e.g., a Customer *places* an Order).

> Example: `Customer` —(places)→ `Order` —(contains)→ `Product` is a simple ER model describing an e-commerce system.

---

## 4. Keys — How Rows Are Uniquely Identified & Linked

| Key Type             | Meaning                                                                                                               | Example                                                                                                  |
|----------------------|-----------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| **Primary Key (PK)** | Uniquely identifies **each row** in a table. No duplicates, no nulls.                                                 | `customer_id` in the `Customer` table                                                                    |
| **Candidate Key**    | Any column (or combination) that *could* serve as the primary key — you pick one to actually be the PK.               | A table might have both `customer_id` and `email` as candidate keys; you choose `customer_id` as the PK. |
| **Foreign Key (FK)** | A column in one table that **references the Primary Key of another table** — this is *how* tables get linked/related. | `customer_id` in the `Order` table, pointing back to `Customer`                                          |
| **Composite Key**    | A primary key made of **two or more columns combined**, when no single column is unique on its own.                   | `(order_id, product_id)` in an `OrderDetails` table                                                      |
| **Natural Key**      | A key based on real, **meaningful business data** (e.g., an email address, a national ID number).                     | `email` as a key                                                                                         |
| **Surrogate Key**    | An **artificial**, system-generated key with no business meaning — usually a simple auto-incrementing integer.        | `customer_id = 10234` (means nothing on its own, just an internal reference)                             |

> **Natural vs. Surrogate — a real trade-off:** Natural keys are meaningful but can **change** (e.g., someone updates their email) or aren't guaranteed unique across systems. Surrogate keys are stable and simple, but require an extra lookup to know what they "mean." **In practice, surrogate keys are strongly preferred** in most database and data warehouse designs, precisely because they never need to change.

---

## 5. Types of Relationships

| Relationship           | Meaning                                                       | Example                                                                                     |
|------------------------|---------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **One-to-One (1:1)**   | One row in Table A relates to exactly **one** row in Table B. | `Employee` ↔ `EmployeeBadge` (each employee has exactly one badge)                          |
| **One-to-Many (1:N)**  | One row in Table A relates to **many** rows in Table B.       | One `Customer` → many `Orders`                                                              |
| **Many-to-Many (N:N)** | Many rows in Table A relate to many rows in Table B.          | Many `Students` ↔ many `Courses` (a student takes many courses; a course has many students) |

**Resolving Many-to-Many**
A N:N relationship **can't be directly represented** in a relational table — it needs a **junction/bridge/associative table** in between, holding foreign keys to both sides.
```
Student(student_id, ...)
Course(course_id, ...)
Enrollment(student_id, course_id, enrollment_date)   -- the junction table
```
> This turns one N:N relationship into two 1:N relationships (Student → Enrollment, Course → Enrollment).

---

# PART 2 — Normalization

## 6. Why Normalize?

**Normalization** is the process of organizing tables to **reduce data redundancy** and avoid **data anomalies**. Without it, the same piece of information gets duplicated across many rows, which causes problems:

| Anomaly            | What goes wrong                                                                                                                                                                                            |
|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Update anomaly** | The same fact (e.g., a customer's address) is stored in multiple rows — update it in one place, forget another, and now the data **contradicts itself**.                                                   |
| **Insert anomaly** | You can't add certain data without also having *unrelated* data available (e.g., can't add a new product without an order for it, if product info is stuffed inside the orders table).                     |
| **Delete anomaly** | Deleting one row accidentally **wipes out unrelated information** you actually wanted to keep (e.g., deleting a customer's only order also deletes their contact info, if it was never stored separately). |

> Example of a **denormalized** (unnormalized) mess: one giant `Orders` table with `customer_name`, `customer_email`, `product_name`, `product_price` repeated on **every single row** for every order — if a customer's email changes, you'd have to update it in hundreds of rows.

## 7. Normal Forms (1NF → 3NF)

Normalization happens in progressive stages, each with stricter rules:

**1NF (First Normal Form)**
- Each column holds **only atomic (single, indivisible) values** — no lists or repeating groups crammed into one cell.
- Each row is unique (has a primary key).
> ❌ Bad: a `phone_numbers` column holding `"9876543210, 9123456780"` in one cell.
> ✅ Fixed: split into separate rows (or a separate related table) — one phone number per row.

**2NF (Second Normal Form)**
- Must already be in 1NF.
- Every **non-key column** must depend on the **entire** primary key — not just part of it (only relevant when using a composite key).
> ❌ Bad: `OrderDetails(order_id, product_id, product_name, quantity)` — here `product_name` depends only on `product_id`, not the full `(order_id, product_id)` key.
> ✅ Fixed: move `product_name` into a separate `Product` table.

**3NF (Third Normal Form)**
- Must already be in 2NF.
- No **non-key column** should depend on **another non-key column** (no "transitive dependency").
> ❌ Bad: `Order(order_id, customer_id, customer_city, customer_state)` — `customer_state` depends on `customer_city`, not directly on `order_id`.
> ✅ Fixed: move city/state into the `Customer` table, referenced via `customer_id`.

> *(Bonus: BCNF — Boyce-Codd Normal Form — is a slightly stricter version of 3NF, used in more advanced/edge-case scenarios; not commonly needed for everyday modeling.)*

## 8. Denormalization — The Deliberate Trade-off

**Denormalization** intentionally **reintroduces some redundancy** — merging normalized tables back together — to make **reads faster**, at the cost of some duplicate storage and more complex updates.

- **Why:** highly normalized data requires many `JOIN`s to answer a query — great for transactional consistency, but can be **slow for analytics/reporting** on large datasets.
- **When to use it:** reporting/analytics systems (data warehouses), read-heavy workloads where query speed matters more than storage efficiency or write simplicity.

> Rule of thumb: **normalize for transactional systems** (accuracy, no duplication), **denormalize for analytical systems** (speed, simpler queries) — this leads directly into the next section.

---

# PART 3 — OLTP vs. OLAP & Dimensional Modeling

## 9. OLTP vs. OLAP

|                      | **OLTP** (Online Transaction Processing)                   | **OLAP** (Online Analytical Processing)                           |
|----------------------|------------------------------------------------------------|-------------------------------------------------------------------|
| **Purpose**          | Day-to-day operations — recording individual transactions  | Analysis, reporting, trends over large volumes of historical data |
| **Example systems**  | An e-commerce checkout system, a banking app               | A sales dashboard, a data warehouse                               |
| **Data model style** | Highly **normalized** (fewer duplicates, fast/safe writes) | Often **denormalized** (dimensional modeling, fast reads)         |
| **Typical queries**  | "Insert this new order," "Update this customer's address"  | "What were total sales by region last quarter?"                   |
| **Read vs. Write**   | Frequent small writes                                      | Fewer, but very large, complex reads                              |

> Simple way to remember: **OLTP = the cash register** (recording each sale), **OLAP = the year-end sales report** (analyzing all the sales together).

## 10. Dimensional Modeling — Facts & Dimensions

**Dimensional Modeling** is the standard approach for designing **OLAP/data warehouse** schemas, built around two core table types:

- **Fact Table** — stores **measurable, quantitative events/metrics** (the "what happened" numbers) — e.g., `sales_amount`, `quantity_sold`, `order_count`. Usually has **many rows** and mostly foreign keys pointing to dimension tables.
- **Dimension Table** — stores **descriptive context** around the facts — the "who, what, where, when" (e.g., `Customer`, `Product`, `Date`, `Store`). Usually has **fewer rows**, but many descriptive columns.

> Example: A `Sales_Fact` table might have `date_id, product_id, store_id, customer_id, quantity_sold, sales_amount` — and each of those `_id` columns points to a corresponding **dimension table** (`Date`, `Product`, `Store`, `Customer`) that holds the descriptive details.

**The Grain of a Fact Table**
The **grain** defines exactly **what one row in the fact table represents** — the single most important design decision when building a fact table.
> Example: Is one row "one line item on a receipt," "one entire order," or "total daily sales per store"? Each is a different, valid grain — but it must be decided clearly and consistently, since it drives everything else about the table's design.

**Types of Fact Tables**

| Type                                 | What it captures                                                                                                                                                     |
|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Transaction fact table**           | One row per individual event/transaction (finest grain, e.g., one row per sale).                                                                                     |
| **Periodic snapshot fact table**     | A row captured at **regular intervals** (e.g., end-of-day account balances), even if nothing changed.                                                                |
| **Accumulating snapshot fact table** | One row per process/entity that gets **updated as it moves through stages** (e.g., an order's row gets updated as it moves from "placed" → "shipped" → "delivered"). |

**Types of Facts (Measures)**

| Type              | Meaning                                                   | Example                                                                                                                                                        |
|-------------------|-----------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Additive**      | Can be summed across **any** dimension.                   | `sales_amount` (safe to sum across time, product, region — all valid).                                                                                         |
| **Semi-additive** | Can be summed across **some** dimensions, but not others. | `account_balance` (summing across time doesn't make sense — you can't "add up" balances over days — but summing across accounts at one point in time is fine). |
| **Non-additive**  | Cannot be meaningfully summed at all.                     | A `ratio` or `percentage` (e.g., profit margin %) — must be recalculated, not summed.                                                                          |

## 11. Star Schema vs. Snowflake Schema

**Star Schema**
- One central **Fact table**, directly connected to **denormalized** Dimension tables (each dimension is a single flat table).
- Simple, fewer joins, **faster to query** — the standard default choice for most data warehouses.
```
        Date
          |
Product — Sales_Fact — Store
          |
       Customer
```

**Snowflake Schema**
- Dimension tables are further **normalized** into sub-dimension tables (e.g., `Product` splits into `Product` + `Category` + `Brand`).
- Saves some storage (less duplication), but requires **more joins**, making queries slightly slower/more complex.
```
Product → Category
Product → Brand
```

> Quick comparison: **Star = simpler & faster, some redundancy.** **Snowflake = more normalized & storage-efficient, more joins needed.** In practice, **Star schema is far more commonly used** for analytics because query speed usually matters more than the storage savings.

## 12. Slowly Changing Dimensions (SCD) — Quick Recap

*(Covered in depth in the Hive notes, since it's commonly taught alongside Hive — brief recap here since it's fundamentally a **data modeling** concept.)*

Describes how to handle changes to dimension data over time:
- **Type 0** — value never changes.
- **Type 1** — overwrite the old value, no history kept.
- **Type 2** — keep full history via new rows (with `effective_date`/`is_current` flags) — the most common approach.
- **Type 3** — keep limited history via an extra "previous value" column.

**A couple of extra SCD types worth knowing (not always covered):**
- **Type 4** — keeps current data in the main dimension table, but moves **historical changes into a separate history table** — keeps the main table small/fast while still preserving full history elsewhere.
- **Type 6** — a **hybrid** combining Types 1, 2, and 3 (overwrite + new row + previous-value column) — used when you need multiple ways of viewing the change at once. Less common, more complex.

## 13. Other Useful Dimensional Modeling Concepts

- **Degenerate Dimension** — a dimension-like value that lives **directly in the fact table** instead of its own dimension table, because it has no other descriptive attributes worth storing separately (e.g., an `invoice_number` or `order_number` — useful for grouping/filtering, but not worth a whole separate table).
- **Junk Dimension** — a single dimension table that **groups together several low-cardinality, unrelated flags/indicators** (e.g., `is_gift_wrapped`, `payment_type`, `is_returned`) that don't deserve their own separate dimension tables — keeps the fact table cleaner.
- **Conformed Dimension** — a dimension table (e.g., `Date`, `Customer`) that's **shared and consistently defined across multiple fact tables/data marts**, so results from different reports/teams stay comparable (e.g., every team uses the exact same `Date` dimension, not their own separate version).
- **Role-Playing Dimension** — a single dimension table used **multiple times in the same fact table for different purposes**, via different foreign keys. Example: a `Date` dimension used as both `order_date_id` and `ship_date_id` in the same fact table — same underlying dimension, different "roles."

---

# PART 4 — Modern & Advanced Approaches

## 14. Data Vault Modeling (Bonus — Advanced)

An alternative modeling approach (popular in large enterprise data warehouses) designed to be highly **flexible to change** and good at preserving **full history and auditability**. Built from three core building blocks:

- **Hub** — stores the **unique list of a core business concept** and its surrogate key (e.g., a `Hub_Customer` table with just `customer_id` and its business key).
- **Link** — stores the **relationships/transactions** between hubs (e.g., a `Link_Order` connecting `Hub_Customer` and `Hub_Product`).
- **Satellite** — stores the **descriptive attributes and their history** for a hub or link (e.g., `Sat_Customer_Details` holding name/address, with full change history over time).

> Why it exists: Data Vault separates **identity** (hubs), **relationships** (links), and **descriptive detail** (satellites) — making it much easier to add new data sources or change business rules later without having to redesign existing tables, unlike star schemas which can require significant rework when the business changes.

## 15. Data Modeling in Modern Data Lakes / Lakehouses

With cloud data lakes (Delta Lake, Iceberg, etc.), modeling philosophy has shifted somewhat:

- **Medallion Architecture** — a common modern pattern organizing data into progressive layers:
  - **Bronze** — raw, unprocessed data, as-is from the source.
  - **Silver** — cleaned, validated, and lightly modeled data (deduplicated, standard types).
  - **Gold** — fully modeled, business-ready data (often dimensional/star-schema style) for direct reporting/analytics use.
- **One Big Table (OBT) / Wide Table approach** — instead of separate fact + dimension tables (star schema), some modern analytics setups **flatten everything into one big denormalized table**. Trades some redundancy/storage for maximum query simplicity and speed — feasible now because cloud storage is cheap and columnar formats (Parquet/ORC) compress repeated values very efficiently.
- **Schema-on-read vs. schema-on-write** — a lakehouse often stores raw data without enforcing a strict schema upfront (schema-on-read, similar to Hive — see the Hive notes), applying modeling/structure **later**, in the Silver/Gold layers, rather than at ingestion time.

> Simple way to see the shift: traditional data warehousing models data **strictly upfront** (schema-on-write); modern data lakes often **ingest first, model later**, giving more flexibility but requiring more discipline in the later transformation layers.

---

## Quick Recap Table

| Term                                    | One-liner                                                                |
|-----------------------------------------|--------------------------------------------------------------------------|
| Conceptual / Logical / Physical Model   | What → how it's structured → how it's actually built                     |
| Entity / Attribute / Relationship       | A "thing" → its property → how two things connect                        |
| Primary / Foreign / Composite Key       | Uniquely IDs a row → links to another table → multi-column unique ID     |
| Natural vs. Surrogate Key               | Meaningful business value vs. artificial, stable system-generated ID     |
| 1:1 / 1:N / N:N                         | One-to-one / one-to-many / many-to-many relationships                    |
| Junction Table                          | Resolves an N:N relationship into two 1:N relationships                  |
| Normalization                           | Organizing data to reduce redundancy & anomalies                         |
| 1NF / 2NF / 3NF                         | Atomic values → full key dependency → no transitive dependency           |
| Denormalization                         | Deliberately reintroducing redundancy for faster reads                   |
| OLTP vs OLAP                            | Transactional day-to-day ops vs. analytical reporting                    |
| Fact Table / Dimension Table            | Quantitative measures vs. descriptive context                            |
| Grain                                   | What exactly one row in a fact table represents                          |
| Additive / Semi-additive / Non-additive | Can always sum / sum sometimes / can't meaningfully sum                  |
| Star vs. Snowflake Schema               | Flat denormalized dimensions vs. further-normalized sub-dimensions       |
| Degenerate Dimension                    | Dimension-like value stored directly in the fact table                   |
| Junk Dimension                          | One table grouping several small unrelated flags                         |
| Conformed Dimension                     | Shared, consistent dimension used across multiple fact tables            |
| Role-Playing Dimension                  | One dimension used multiple times for different purposes in a fact table |
| SCD (Type 0–6)                          | Strategies for handling dimension data that changes over time            |
| Data Vault (Hub/Link/Satellite)         | Flexible, history-preserving alternative to star schema                  |
| Medallion Architecture                  | Bronze (raw) → Silver (cleaned) → Gold (business-ready) data layers      |
| One Big Table (OBT)                     | Flattened, denormalized alternative to star schema                       |

