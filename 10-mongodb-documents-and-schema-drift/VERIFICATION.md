# Live re-verification — 2026-11-08

Status: **PARTIALLY FIXED — LAB STILL BLOCKED**.

Tested the published hydra-etl 0.19.1 package in an isolated Python 3.13
virtual environment, with PyMongo 4.19.0 and a real local MongoDB 7.0 container.
The imported package path and version were checked outside the engine checkout.
No engine code was modified. No commands were executed on Killercoda.

## Fixed behavior

The original boundary probe now passes: SourceParser/JobExecutor forwards the
schema, warn emits a drift warning, fail raises SchemaDriftError at document 101,
and adapt retains the new field in the connector output.

## Blocker 1: the original job cannot start extraction

All three original jobs fail with:

```text
ValueError: source extract must define 'table' or 'query'
```

The MongoDB source declares `extract.collection: orders`, as expected by its
connector, but JobExecutor._resolve_extract_options requires table or query.
The engine must accept collection-based sources through this execution path.

For diagnosis only, a fresh temporary copy added `table: orders` alongside
`collection: orders`. The repository's source template was not changed.

## Blocker 2: adapt loses the added field in the complete transfer

With that temporary YAML adjustment, the actual CLI produced:

| Policy | CLI exit | CSV rows | Observed result | Acceptance |
| --- | ---: | ---: | --- | --- |
| warn | 0 | 102 | Drift warning; original three columns | PASS |
| fail | 1 | 0 | SchemaDriftError names sales_channel at document 101; no CSV output | PASS |
| adapt | 0 | 102 | CSV contains only _id, customer, amount; sales_channel is missing | FAIL |

A separate direct extraction from the same real MongoDB server confirms that
adapt returns sales_channel=web for ORD-101 and sales_channel=store for ORD-102.
The first record still has only the original three keys. Thus adaptation works
at the connector boundary, but the new field is lost downstream in the complete
MongoDB-to-CSV transfer. The precise downstream cause needs investigation;
this report does not attribute it to a specific writer implementation.

Reproduction fixture: 100 baseline documents followed by two documents adding
sales_channel; schema.mode=infer_strict, sample_size=100, extract.batch_size=1000.
Expected adapt result: 102 rows, four columns, both new values preserved, and
empty cells for the 100 documents without the new field.

The lab remains pinned to 0.16.0. Changing that pin to 0.19.1 alone is insufficient.
Do not publish the lab as working until both complete-transfer blockers pass.
Linux/Killercoda startup was not retested in this audit.

## Local evidence

Evidence is retained under the Codex visualization workspace
`C:/Users/DELL/.codex/visualizations/2026/10/29/01a1885f-418d-77e0-bb96-b6816681834f`:

- `lab10-audit-0191-project/evidence`: original jobs, CLI logs and JSON results.
- `lab10-audit-0191-table/evidence`: temporary table+collection jobs, CLI logs and JSON results.
- `lab10-audit-0191-table/jobs/*/output`: generated CSV files.
- `lab10-audit-0191-table/direct-live-adapt.json`: direct real MongoDB extraction.

The temporary MongoDB audit container was stopped after testing.

---

# Historical verification (0.16.0)

# Verification — LAB lab-02-03

Date: 2026-10-31. Status: **BLOCKED DRAFT**.

## Reproduced engine blockers

Tested against installed hydra-etl 0.16.0 in an isolated Python 3.13 environment
on Windows. MongoDB driver: PyMongo 4.19.0. No Hydra engine files were modified.

The real SourceParser accepts the YAML schema, but JobExecutor._build_connector
does not include it in the connector configuration.

The extraction probe supplies that schema directly to the real MongoDBConnector,
isolating extraction behavior from the forwarding defect. Only the database cursor
is replaced by an in-memory fixture (100 baseline documents, then two changed ones).

| Requested policy | Rows extracted | Drift warning | Exception | New values preserved |
| --- | ---: | --- | --- | --- |
| warn | 102 | No | No | No |
| fail | 102 | No | No | No |
| adapt | 102 | No | No | No |

This is not a live database or complete CLI execution test. A fix to schema
forwarding alone is insufficient to make the comparison work.

## Relevant engine paths

- `hydra_etl/internal/runner/executor.py`: _build_connector omits schema.
- `hydra_etl/plugins/connectors/mongodb/connector.py`: _ensure_schema samples
  100 documents; extract_batches normalizes without invoking drift validation.
- `hydra_etl/internal/schema/validator.py`: validation can report extra fields,
  but is not wired into MongoDB extraction; adapt does not expand the schema here.

The chapter's intended behavior therefore cannot be advertised as working in 0.16.0.

## Scope of acceptance checks

Local checks completed successfully:

- `tests/check_offline.py`: fixture integrity, scenario references, all three
  generated jobs accepted by `hdrctl validate`, rejection of misleading outputs,
  and refusal to overwrite an existing project.
- `bash -n`: all five setup/step shell scripts.
- `docker compose config --quiet`: the MongoDB service definition.
- `assets/probe.py`: reproduced the blocker, exiting 1 as expected (not a pass).

The offline test checks fixture boundaries, manifest parsing through the actual CLI,
scenario references, and rejection of misleading results (silent warn, successful
fail, unrelated failure, or adapt losing the new values).

The startup probe checks both source-schema forwarding and real connector behavior.
It stops the scenario before MongoDB startup when the feature is unavailable.

The live helper runs the actual CLI, preserves logs and exit codes, and checks the
output against the fixture. It never implements schema adaptation itself.

Live MongoDB seeding, Linux setup, and complete CLI transfer remain unverified.
Do not treat offline checks or a successful YAML validation as proof of drift support.
