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
