# Looker — Revision Notes for a Lead Data Engineer (80/20 Approach)

*As a Lead Data Engineer, your job on a Looker project is mostly about the **modeling layer, architecture, governance, and performance** — not building dashboards or picking chart colors. These notes are scoped to the ~20% of Looker that will cover ~80% of what you're actually expected to own/review.*

---

## 0. Where You Should Focus vs. Skip

| Focus HARD on this (your actual job)                     | You can go LIGHT on this (analyst/BI-dev territory) |
|----------------------------------------------------------|-----------------------------------------------------|
| LookML architecture: Models, Views, Explores             | Building dashboards & choosing chart types          |
| Joins, derived tables, performance                       | Formatting, colors, dashboard layout                |
| Governance: access control, row-level security           | Ad-hoc "Explore" self-service usage patterns        |
| Git-based dev workflow & deployment                      | Looker Blocks / marketplace templates               |
| Connection setup & warehouse interaction                 | Scheduling/alerting UI details                      |
| Understanding the new AI/semantic-layer direction (2026) | Deep visualization API customization                |

> As a lead, you'll be judged on: **is the data model correct, performant, secure, and maintainable** — not on whether the dashboard looks pretty.

---

## 1. What Is Looker?

**Looker** (part of Google Cloud) is a **BI (Business Intelligence) platform built around a semantic modeling layer**. It doesn't move or copy your data — it sits **directly on top of your existing data warehouse** (BigQuery, Snowflake, Redshift, etc.) and translates business questions into SQL on the fly.

- Looker's core differentiator is **LookML** — its own modeling language, where metrics/dimensions/joins are defined **once, in code**, and reused everywhere (dashboards, self-service exploration, API calls).
- This solves the classic BI problem of "two dashboards, two different numbers for revenue" — because everyone queries through the **same governed semantic layer**, not through 20 different hand-written SQL queries.
- Models are stored in a **Git repository** — meaning standard software engineering practices apply: version control, code review, branching, CI/CD-style validation.

> Simple mental model: **LookML = the contract between your warehouse and every human/AI that asks it a question.** Get this layer right, and everything downstream (dashboards, self-serve, AI agents) inherits correct, consistent numbers automatically.

**Don't confuse it with:**
- **Looker Studio** — a *separate*, free, lightweight Google product (formerly Google Data Studio) with basic drag-and-drop dashboards — **no LookML, no real semantic layer**. If your requirement mentions "Looker Studio," that's a much simpler tool than what these notes cover.

---

## 2. Core Architecture — The Three File Types

Everything in LookML is built from three main file types, working together:

| File                           | Purpose                                                                                                                                                                                        |
|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **View file (`.view.lkml`)**   | Defines a **single table (or derived table)** — its dimensions, measures, and how it can join to others. This is your closest equivalent to defining a table's "shape" in a data model.        |
| **Model file (`.model.lkml`)** | Ties views together — declares the **database connection**, and defines **Explores** (which views are joined together and how).                                                                |
| **Explore**                    | A defined **starting point for querying** — essentially a pre-joined, business-user-friendly "virtual table" built from one or more views. This is what business users actually interact with. |

> Relationship: **Views = your building blocks (like normalized tables). Explores = pre-assembled joins of those blocks, exposed to end users.** A Model file is basically the "menu" listing which Explores are available and how they connect to a database connection.

---

## 3. LookML Building Blocks

**Dimension**
A column-level attribute you can group/filter by — the "descriptive" side of data (similar to a dimensional-modeling dimension attribute).
```lookml
dimension: customer_name {
  type: string
  sql: ${TABLE}.customer_name ;;
}
```

**Measure**
An aggregated, calculated value — the "metric" side (sum, count, average, etc.) — conceptually the same as a "fact/measure" in dimensional modeling.
```lookml
measure: total_revenue {
  type: sum
  sql: ${TABLE}.order_amount ;;
}
```

**Join**
Defines how two views relate — this is where your data-modeling knowledge directly transfers. Get the join type and relationship (`one_to_many`, `many_to_one`, etc.) wrong, and you'll silently **fan-out or double-count** aggregates — a classic, very real production bug in Looker.
```lookml
explore: orders {
  join: customers {
    type: left_outer
    sql_on: ${orders.customer_id} = ${customers.customer_id} ;;
    relationship: many_to_one
  }
}
```

**Derived Tables**
LookML lets you define a view's SQL logic **directly as a query** rather than pointing at a raw table — effectively an in-model transformation layer.
- **SQL-based derived table** — you write custom SQL that becomes the "table" the view is built from.
- **Persistent Derived Table (PDT)** — Looker actually **materializes** this derived table into a real (temporary) table in your warehouse (or a dedicated scratch schema) on a schedule/trigger, rather than recomputing it on every query. This is a **major performance lever** — the closest LookML equivalent to a pre-aggregated table or materialized view.

> As a data engineer, PDTs are one of the areas where you'll have the most direct influence — deciding what should be pre-aggregated in the warehouse (via dbt, etc.) vs. what should be a PDT vs. what should just be computed live.

---

## 4. Symmetric Aggregates (Why Looker Handles Joins Differently)

Worth understanding conceptually, since it's a common source of confusion coming from plain SQL: when Looker joins a "one" table to a "many" table and then aggregates a measure from the "one" side, a naive `JOIN` + `SUM` would **inflate the result** (because rows get duplicated by the join). Looker's SQL generation automatically uses techniques (symmetric aggregates) to **avoid this double-counting**, so a `SUM` stays correct even across a fan-out join.

> You don't need to hand-write this — just know it exists and *why* it exists, so you're not surprised when Looker's generated SQL looks more complex than a simple `JOIN + GROUP BY`.

---

## 5. Development Workflow — Git-Based

This is where your engineering background matters most:

- LookML projects live in a **Git repository** (GitHub, GitLab, etc.) — real version control, not a black-box UI.
- Developers work in **personal development branches**, test changes in a **Dev Mode** sandbox, then merge/deploy to **Production**.
- **LookML Validator** — checks for syntax errors and broken references before deployment.
- Supports standard **CI/CD practices** — automated testing (Looker has a `content-validator`/`lookml-validator` API), PR review, and controlled promotion to production — treat it like any other codebase your team owns.

> As a lead, this is an area to actively set standards on: branching strategy, required reviews before merging to a shared model, and whether you run any automated LookML validation in CI.

---

## 6. Governance & Access Control

This is a major reason organizations choose Looker over simpler tools, and a major reason it lands on a *data engineer's* plate rather than purely an analyst's:

- **Access Grants / Access Filters** — restrict which rows a user can see based on their attributes (e.g., a regional sales rep only sees their own region's data) — **row-level security defined in LookML**, not bolted on afterward.
- **Model/Explore-level permissions** — control which teams can even see/query a given Explore at all.
- **Content permissions** — control who can view/edit specific dashboards/folders.
- Because metric definitions live in **one governed place**, you avoid the classic problem of different teams building slightly different "active user" definitions in separate BI tools.

---

## 7. Performance Considerations (Where a Data Engineer Adds Real Value)

- **PDTs (see §3)** — pre-materialize expensive/frequently-used aggregations.
- **Caching** — Looker caches query results for a configurable duration, reducing redundant warehouse load.
- **Aggregate Awareness / Aggregate tables** — LookML can be configured to automatically route a query to a smaller, pre-aggregated table when the requested grain allows it, instead of always hitting the raw, large fact table.
- **Warehouse-side modeling still matters** — Looker doesn't replace good warehouse modeling (star schemas, proper partitioning/clustering in BigQuery/Snowflake, etc. — see your Data Modeling notes). LookML sits *on top of* a well-modeled warehouse; it isn't a substitute for one. Bad upstream modeling = slow, messy LookML no matter how well the LookML itself is written.

---

## 8. Connections — How Looker Talks to the Warehouse

- A **Connection** (defined at the admin/model level) tells Looker which database/warehouse to query, and how (credentials, connection pool settings, etc.).
- Looker **does not store your actual data** (aside from PDT materializations and cache) — every Explore query generates **live SQL** sent to your actual warehouse.
- Supports most major cloud warehouses: **BigQuery, Snowflake, Redshift, Databricks**, and more.

---

## 9. What's New/Relevant in 2026 (Worth Knowing for a Current Requirement)

Looker's direction has shifted meaningfully — worth being aware of since a "requirement" today likely touches these:

- **AI/Gemini Integration** — Looker is increasingly positioned as the **grounding layer for AI agents**, not just human dashboards. Gemini-powered features include natural-language querying ("Conversational Analytics"), automated LookML authoring assistance, and "Dashboard Agents."
- **Headless BI / Managed MCP** — Looker now exposes its semantic layer to **external tools/agents** (e.g., Claude Desktop) via a **Managed MCP (Model Context Protocol)** offering — meaning LookML's governed metrics can now be queried by AI assistants outside Looker's own UI entirely, not just inside dashboards.
- **Expanded semantic modeling** — LookML is being extended to support **graph-based models** (e.g., BigQuery Graph) and integrate with **Snowflake Semantic Views**, pushing it beyond flat table-based modeling into more complex ontologies.
- **Competitive context** — you'll likely see LookML compared against **dbt Semantic Layer** and **Cube** in any serious 2026 architecture discussion. Rough framing:
  - **LookML** — best if Looker is already your org's governed BI/dashboarding tool; strong governance, but ties you to the Looker ecosystem (vendor lock-in is the main trade-off).
  - **dbt Semantic Layer** — best if your metric logic should live inside your dbt project, closer to the transformation layer itself.
  - **Cube** — best for a **headless** semantic layer serving APIs/embedded analytics/multiple BI tools at once, not tied to one BI front-end.

> If your requirement is evaluating *whether* to adopt Looker (vs. build vs. buy alternatives), this trade-off — **governance & BI-native integration vs. ecosystem lock-in** — is the crux of the decision, and is exactly the kind of judgment call a Lead Data Engineer is expected to weigh in on.

---

---

# Interview Prep — Q&A (Basic → Advanced → Lead-Level)

*80/20 applied here too: these questions cover the ones most likely to actually come up for a Lead Data Engineer role — conceptual understanding + judgment calls, not obscure LookML syntax trivia.*

## Level 1 — Basics (Make sure you can answer these instantly)

**Q1. What is Looker, in one sentence?**
A: Looker is a BI platform built around a code-based semantic modeling layer (LookML) that sits on top of a data warehouse, translating business questions into governed, consistent SQL — rather than storing or moving the data itself.

**Q2. What is LookML?**
A: Looker's proprietary modeling language, used to define dimensions, measures, joins, and business logic in version-controlled code, so metrics are defined once and reused consistently across every dashboard, Explore, and API call.

**Q3. What's the difference between a Model, a View, and an Explore?**
A: A **View** defines a single table's dimensions/measures. A **Model** declares the database connection and lists the available Explores. An **Explore** is a pre-joined, business-user-facing "virtual table" built from one or more Views.

**Q4. What's the difference between a dimension and a measure?**
A: A **dimension** is a groupable/filterable attribute (e.g., `customer_name`, `order_date`). A **measure** is an aggregated calculation (e.g., `sum(order_amount)`, `count(orders)`).

**Q5. How does Looker connect to data — does it store the data itself?**
A: No. Looker connects to your existing warehouse (BigQuery, Snowflake, Redshift, Databricks, etc.) via a **Connection**, and generates SQL live for each query. It doesn't copy/store your data, aside from cached results and any Persistent Derived Tables (PDTs) it's configured to materialize.

**Q6. What's the difference between Looker and Looker Studio?**
A: They're different products. **Looker Studio** (formerly Google Data Studio) is a free, simple drag-and-drop dashboarding tool with **no LookML/semantic layer**. **Looker** is the enterprise platform with a full governed modeling layer (LookML), Git-based development, and access control.

---

## Level 2 — Intermediate (Core day-to-day working knowledge)

**Q7. How do you define a join between two views in LookML? What does `relationship` control?**
A: Inside an `explore` block, using a `join` with `sql_on` (the join condition) and `type` (e.g., `left_outer`). `relationship` (e.g., `many_to_one`, `one_to_many`, `many_to_many`) tells Looker the cardinality of the join — this is critical, because it affects how Looker aggregates measures correctly (see symmetric aggregates, Q13).

**Q8. What is a derived table, and what's the difference between a regular derived table and a Persistent Derived Table (PDT)?**
A: A derived table lets you define a View's data using a custom SQL query instead of pointing directly at a raw table. A regular derived table is recomputed as part of each query. A **PDT** is materialized — Looker actually creates a real (temporary/scratch) table in the warehouse on a schedule or trigger, so expensive logic doesn't need to be recomputed on every single query. PDTs are a major performance lever.

**Q9. What triggers a PDT rebuild?**
A: Configurable — commonly `sql_trigger_value` (rebuild when a query, like `SELECT MAX(updated_at)`, returns a new value), a fixed time-based schedule (`datagroup_trigger`), or on every query (rare, defeats the purpose). Datagroups are the more modern/recommended mechanism — they define a shared caching/rebuild policy multiple PDTs and Explores can reference.

**Q10. What is caching in Looker, and why does it matter?**
A: Looker caches query results for a configurable duration so repeated identical queries don't have to re-hit the warehouse — reduces both latency for users and cost/load on the warehouse. Cache policies can be tied to datagroups, similar to PDT triggers.

**Q11. What are Access Filters / Access Grants, and why would a data engineer care about them?**
A: They implement **row-level security directly in LookML** — restricting which rows a user can see based on attributes tied to their account (e.g., a regional manager only sees their region's data). As a data engineer, you're often the one responsible for designing this correctly and making sure it can't be bypassed — a governance and security concern, not just a modeling one.

**Q12. Describe Looker's typical development workflow.**
A: LookML lives in a Git repo. Developers work in personal Dev Mode branches, validate changes (LookML Validator catches broken references/syntax errors), then merge and deploy to Production — similar to any standard software engineering branching/review/CI workflow.

---

## Level 3 — Advanced (Where you separate yourself from a mid-level analyst/BI dev)

**Q13. What are "symmetric aggregates," and why does Looker need them?**
A: When Looker joins a "one" side table to a "many" side table and then aggregates a measure from the "one" side, a naive `JOIN` + `SUM` would double-count rows because of the fan-out from the join. Looker's SQL generation automatically applies a technique (symmetric aggregates) to prevent this inflation, so a `SUM` stays correct even across a fan-out join — without you needing to hand-write de-duplication logic.

**Q14. A dashboard's numbers look inflated/wrong after adding a new join. What's your diagnostic approach?**
A: This is a classic fan-out symptom. I'd check: (1) the `relationship:` type declared on the join — is it actually `many_to_one` when it should be, or is it silently causing a one-to-many explosion; (2) whether the measure being summed lives on the "many" side of a fan-out join without symmetric aggregate protection kicking in correctly; (3) look at the generated SQL (Looker exposes this) to see the actual join and aggregation logic Looker produced, rather than guessing from the dashboard number alone.

**Q15. What is Aggregate Awareness, and when would you use it?**
A: A feature where LookML can be configured with pre-aggregated summary tables, and Looker automatically routes a query to the smaller aggregate table instead of the full raw fact table, when the requested grain allows it — similar in spirit to materialized-view query rewriting. Use it when you have very large fact tables and users commonly query at a coarser grain than the raw data (e.g., daily/monthly rollups instead of row-level).

**Q16. How would you approach modeling a very large fact table in LookML for good performance?**
A: This is fundamentally a **warehouse modeling problem first, LookML problem second**: ensure the underlying table is well-partitioned/clustered (e.g., by date in BigQuery), pre-aggregate common grains upstream (via dbt or a PDT), use Aggregate Awareness for common summary grains, and be deliberate about which dimensions/joins are exposed in the Explore so users aren't accidentally triggering expensive fan-out joins on ad-hoc exploration.

**Q17. What's the difference between a `datagroup` and a manually-set PDT trigger?**
A: A `datagroup` centralizes a caching/rebuild policy that multiple PDTs (and Explore-level caching) can reference — so you define the "how fresh does this data need to be" logic once, rather than repeating trigger logic across many individual PDTs. It's the more maintainable, DRY approach at scale.

**Q18. How does Looker handle liquid templating / conditional logic in LookML?**
A: LookML supports **Liquid templating** (a templating language) to make SQL dynamic based on filter context, user attributes, or other runtime values — e.g., changing a filter's behavior based on which user attribute is set, or conditionally including SQL logic. Useful for advanced access-filtering or reusable, parameterized logic, though it adds real complexity and should be used sparingly/deliberately.

**Q19. How do you handle a scenario where two teams define the same metric (e.g., "active user") differently?**
A: This is exactly the problem LookML's centralized semantic layer is meant to solve — the fix is organizational as much as technical: establish a **single, governed definition** (owned by a clear team, e.g., a shared "core" Explore/View both teams inherit from), document it, and route both teams' dashboards through that shared definition rather than allowing parallel, locally-defined measures with the same name to drift apart.

---

## Level 4 — Lead / Architecture / Judgment Questions

*(These are where a Lead Data Engineer interview actually differentiates you — expect open-ended, "how would you decide" style questions.)*

**Q20. When would you choose Looker/LookML over dbt Semantic Layer or Cube for a new project?**
A: Depends on where the org's center of gravity already is. **LookML** makes sense if Looker is already (or will be) the primary BI/dashboarding tool and you want tight governance built into the same platform users query from. **dbt Semantic Layer** makes more sense if metric ownership should live inside the transformation/dbt workflow, closer to where the data is actually modeled. **Cube** fits best when you need a **headless** semantic layer serving multiple BI tools, embedded analytics, or APIs — not tied to one BI front-end. The real trade-off to articulate: LookML gives strong native governance but ties you to the Looker ecosystem (vendor lock-in); a headless layer gives more flexibility but more infrastructure to own yourself.

**Q21. How would you structure a LookML codebase for a large organization with many teams?**
A: Break Views/Explores along clear domain boundaries (e.g., per business area), promote **shared/conformed dimensions** (like a single `Date` or `Customer` view reused across domains — same idea as a conformed dimension in a data warehouse), enforce code review on any shared/core model changes, and use folder/project structure plus access permissions so teams can move independently on their own Explores without constantly colliding on shared files.

**Q22. How do you manage LookML changes safely in production — what does your release process look like?**
A: Git-based branching (feature branches per developer), Dev Mode for isolated testing against real data, mandatory LookML Validator pass + peer review before merge, and a controlled deploy to Production — ideally with some automated regression check (e.g., content validation to catch dashboards broken by a renamed field) before or immediately after deploy.

**Q23. A migration project requires moving from [some other BI tool] to Looker. What's your approach as the lead?**
A: I'd prioritize: (1) inventorying and prioritizing the **highest-value/most-used metrics and dashboards** first rather than a full 1:1 migration; (2) establishing the **core conformed dimensions/facts** in LookML early, since everything else builds on that foundation; (3) running the old and new systems **in parallel** for validation on key metrics before cutover, to catch definitional drift; (4) treating it as an opportunity to **clean up inconsistent metric definitions** discovered during migration, rather than blindly replicating old, possibly inconsistent logic.

**Q24. How do you think about cost/performance trade-offs with Looker on a cloud warehouse (e.g., BigQuery/Snowflake)?**
A: Every uncached Explore query is live warehouse compute — so cost management is really warehouse-query-cost management. Levers: PDTs/aggregate tables to avoid repeatedly scanning large raw tables, sensible caching/datagroup policies so identical queries aren't re-run unnecessarily, good warehouse-side partitioning/clustering, and being deliberate about which large fact tables are exposed for unrestricted ad-hoc exploration vs. locked down to specific pre-built Explores.

**Q25. How does Looker fit into the newer trend of AI agents querying data directly (2026 context)?**
A: Looker is positioning its semantic layer as the **grounding layer for AI**, not just human dashboards — via Conversational Analytics (natural-language queries answered through the governed LookML layer) and a **Managed MCP** offering that exposes LookML's governed metrics to external AI agents/tools (e.g., Claude) outside Looker's own UI. As a lead, the implication is that a well-governed semantic layer becomes even more valuable — it's the guardrail that keeps an AI agent from inventing/hallucinating a metric definition, since the agent is forced to query through the same governed logic every dashboard already uses.

**Q26. What's a mistake you'd watch out for when a team is new to LookML?**
A: Over-modeling everything as one giant Explore with too many joins available, which invites accidental fan-out/performance problems and confuses self-serve users with too many options. I'd push for **narrower, purpose-built Explores** with clearly scoped joins, rather than one "do everything" Explore that's technically flexible but operationally risky.

---

## Interview Prep — Quick-Reference Cheat Sheet

| If asked about...                      | Anchor your answer on                                          |
|----------------------------------------|----------------------------------------------------------------|
| What Looker is                         | Semantic layer on top of the warehouse, not a copy of the data |
| LookML structure                       | View → Model → Explore, and how they relate                    |
| Performance                            | PDTs, datagroups, aggregate awareness, warehouse-side modeling |
| Correctness bugs                       | Fan-out joins & symmetric aggregates                           |
| Security                               | Access filters = row-level security in code                    |
| Process                                | Git workflow: branch → validate → review → deploy              |
| Governance/strategy                    | One conformed metric definition, reused everywhere             |
| Tool choice (LookML vs dbt SL vs Cube) | Governance & lock-in vs. flexibility & headless delivery       |
| Where this is heading                  | AI grounding layer — Conversational Analytics, Managed MCP     |

---

## Quick Recap Table — Concepts

| Term                           | One-liner                                                                                        |
|--------------------------------|--------------------------------------------------------------------------------------------------|
| LookML                         | Looker's code-based modeling language — defines metrics/dimensions/joins once, reused everywhere |
| View                           | Defines one table's dimensions & measures                                                        |
| Model                          | Declares the DB connection & available Explores                                                  |
| Explore                        | A pre-joined, business-user-facing "virtual table"                                               |
| Dimension / Measure            | A groupable attribute / an aggregated metric                                                     |
| PDT (Persistent Derived Table) | A LookML-defined query materialized as a real table for performance                              |
| Symmetric Aggregates           | How Looker avoids double-counting when aggregating across fan-out joins                          |
| Access Filters                 | Row-level security defined directly in LookML                                                    |
| Connection                     | Config telling Looker which warehouse to query, and how                                          |
| Conversational Analytics       | Natural-language querying grounded in the LookML semantic layer                                  |
| Managed MCP                    | Exposes Looker's governed semantic layer to external AI agents/tools                             |
| Looker Studio                  | A *separate*, free, simpler Google BI tool — no LookML/semantic layer                            |

