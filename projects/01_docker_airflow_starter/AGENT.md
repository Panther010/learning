# AGENT.md — Instructions for AI Coding Agents on This Project

This file is for whichever AI agent (Claude Code, Codex, etc.) is generating code
for this project. The project owner is **learning Docker and Airflow from zero**
while already being comfortable with PySpark. Optimize for teaching, not just
working output.

## Read First
Read `PLAN.md` in this same directory before doing anything. It defines the phases,
directory structure, and checkpoints. Do not skip ahead to a later phase without
being explicitly asked.

## Core Working Rules

1. **One phase at a time.** Only generate files for the phase currently being
   worked on. If asked to "just do the whole thing," push back and suggest doing
   it phase by phase instead — that's the explicit point of this project.

2. **Explain, don't just emit.** For every Docker or Airflow concept used
   (volumes, operators, DAG dependency syntax, connections, XComs, etc.), add an
   inline comment explaining *what it does and why it's needed here* — the
   project owner is learning these tools, not just PySpark. PySpark-only code
   doesn't need this treatment; assume PySpark competence already exists.

3. **Standalone-first for Spark scripts.** Every script in `spark_jobs/` must be
   runnable directly with `python script.py` or `spark-submit script.py` outside
   of Airflow, for debugging. Put Airflow-specific wiring only in `dags/`, never
   inside the Spark job scripts themselves.

4. **No silent scope creep.** Don't add extra tables, extra DAGs, extra
   abstractions, or "nice to have" infra (e.g. a metastore, a message queue,
   Kubernetes) unless asked. This is a learning project — extra moving parts add
   confusion, not value, unless the plan calls for them.

5. **Bronze never drops data.** Bronze-layer scripts must not filter, dedupe, or
   "fix" bad rows — only add ingestion metadata and write out. Any cleaning
   belongs in Silver. If asked to add cleaning logic to a bronze script, flag
   this to the user before doing it.

6. **Quarantine, don't discard.** When Silver-layer logic drops rows (corrupted
   data, failed validation), write those rows to a `_rejects/` path rather than
   silently dropping them.

7. **Every generated file needs a one-paragraph summary in chat** (not just in
   code comments) explaining: what the file does, what it depends on, and what
   command to run to test it standalone before wiring it into Airflow.

## Review Protocol

The project owner reviews every file before running it. To make review easy:

- Keep diffs/files small and single-purpose. Don't bundle unrelated changes.
- When modifying `docker-compose.yaml`, show a summary of exactly what changed
  and why (e.g. "added a volume mount for `spark_jobs/` so Airflow's worker can
  see your scripts") — don't just silently regenerate the whole file.
- Flag any command that will download something (Docker images, pip packages)
  before running it, since these can be slow/large.
- Never invent AWS/GCP/cloud credentials, external service calls, or network
  dependencies beyond what the plan specifies (this is a local-only project).

## Conventions

- **Language:** Python for all Spark jobs and DAGs.
- **Style:** PEP8, type hints on function signatures in `spark_jobs/`.
- **Paths:** always reference data paths via a single config source
  (e.g. `spark_jobs/utils/spark_session.py` or environment variables set in
  `docker-compose.yaml`), never hardcode absolute paths inside job scripts.
- **Naming:** Bronze/Silver/Gold tables use the names given in `PLAN.md`'s
  directory structure — don't rename them ad hoc.
- **DAG IDs:** match the phase name, e.g. `bronze_ingest_dag`,
  `silver_transform_dag`, `gold_aggregate_dag`.
- **Spark session:** build via a single shared helper
  (`spark_jobs/utils/spark_session.py`) so config (app name, shuffle partitions,
  etc.) is consistent across jobs, not copy-pasted into every script.

## Docker/Airflow Version Policy

- Use the current stable Apache Airflow release's official reference
  `docker-compose.yaml` as the Phase 2 starting point rather than writing one
  from scratch — adapt it, don't reinvent it.
- Pin versions explicitly in `requirements.txt` and the Dockerfile (no
  unpinned `latest` tags) so the environment is reproducible.
- If a version choice matters for compatibility (e.g. PySpark version vs Java
  version), state the constraint explicitly rather than assuming.

## What NOT to Do

- Don't auto-run `docker-compose up` or any long-lived/background process
  without the project owner explicitly asking for it in that turn.
- Don't fabricate sample data or synthetic rows — always operate on the real
  4 CSVs provided.
- Don't collapse Bronze/Silver/Gold into fewer layers "for simplicity" — the
  three-layer separation is itself part of what's being learned.
- Don't introduce a full Spark cluster (multiple worker containers) before
  Phase 3's "Option A" (single-container spark-submit) has been proven to work.
- Don't skip writing the standalone-runnable version of a Spark script even if
  the DAG wiring feels faster to write directly.
- do not use emojis in code or file

## When Stuck or Ambiguous

If a requirement in `PLAN.md` is ambiguous (e.g. the country-identity SCD
decision in Phase 5), do not silently pick an approach — state the tradeoff in
one or two sentences and ask, or pick a clearly-labeled default and say so
explicitly so it's easy to revisit later.

## Definition of Done Per Phase

A phase is done when:
1. All files listed for that phase in `PLAN.md` exist.
2. The phase's "Checkpoint" in `PLAN.md` has been verified by the project owner.
3. The `PLAN.md` status checklist has been updated (agent may propose the edit;
   project owner confirms).
