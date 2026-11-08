# Verification — LAB lab-02-05

Finalized: 2026-11-08. Status: **local Linux walkthrough passed**.
Awaiting user review and publication. No Killercoda session was accessed.

## Environment

- Ubuntu 24.04 test container with Python 3.12.
- Published Hydra ETL 0.19.1 and its MySQL driver installed by background.sh.
- New dedicated MySQL 8.4 container, database shop, localhost port 3313.
- Plain Docker startup through an isolated test engine; no Docker Compose.
- Existing Linux test host reused, but the lab12 project and MySQL database were new.
- No Hydra engine code changed.

## Actual walkthrough

The background setup installed dependencies, prepared data and demo secrets,
started MySQL, waited for authenticated access, seeded the table, verified the
initial state, and wrote the ready marker.

tests/run_lesson.py executed the exact executable commands from all four lesson
pages. It confirmed that jobs/products initially contained no YAML files.

| Step | Observed result |
| --- | --- |
| 1 | Learner commands created sources.yaml and transformations.yaml; Check passed. |
| 2 | Learner commands created destinations.yaml and pipeline.yaml; real CLI validation and Check passed. |
| 3 | Actual first Hydra run succeeded; four exact rows verified; first-run checkpoint saved. |
| 4 | Source helper changed SKU-002; actual second run succeeded; four exact rows verified; Check passed. |

First-run rows:
- SKU-001: Notebook, 12.50, quantity 4 (existing row updated).
- SKU-002: Keyboard, 29.95, quantity 3 (inserted).
- SKU-003: Mouse, 8.75, quantity 6 (inserted).
- SKU-099: Legacy product, 5.00, quantity 1 (preserved).

Second-run rows: exactly the same four SKUs, with SKU-002 changed to
Keyboard Pro, 34.95, quantity 7. All other values were unchanged.

## Negative checks and packaging

- Check rejected the initially empty job directory.
- First-run check failed before the first load.
- Second-run check failed after the CSV change but before the second load.
- Repeating the source-update helper was rejected; existing work was preserved.
- Startup-message tests passed: ready, failed, timeout, missing assets.
- Bash syntax checks passed for setup, asset scripts, and all step verify scripts.
- Python syntax and scenario file references were checked.
- Dependency pins match in requirements.txt and assets/requirements.txt.
- Solution YAML files are not deployed as assets; the learner creates all four files.

## Limits

The full startup, lesson commands, real database writes, and verification scripts
were tested locally under Linux. This does not establish that the new scenario has
already been delivered or tested on Killercoda. After publication, use a fresh
session and only the normal lesson commands. No extra diagnostic commands are
required from the learner.
