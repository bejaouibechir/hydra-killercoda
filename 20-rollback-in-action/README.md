# 20 — Rollback in action

Killercoda lab for `LAB lab-03-03` in `03-workflows.md`. The project has two CSV → PostgreSQL `replace` jobs and a third Python action that fails intentionally. A normal run restores both baseline tables. A second run adds one sentinel payment from the failing action, causing the actual Hydra rollback guard to stop. The learner removes only that sentinel and uses `hdrctl workflow undo rollback_demo` to resume.

The lab uses the published `hydra-etl[postgres]==0.19.1`, a dedicated PostgreSQL container on 127.0.0.1:5443, and the dedicated `lab20` schema. Setup has a ready marker; Check scripts read only this lab's reports, schema and journal. Do not run checks or diagnostic commands outside this scenario on Killercoda.

Local review precedes any commit or push.
