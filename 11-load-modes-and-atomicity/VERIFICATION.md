# Verification — LAB lab-02-04

Date: 2026-11-04. Status: **local PostgreSQL integration checks passed**.
Pending: user review, explicit publication approval, and a fresh Killercoda session.

## Environment

- Installed Hydra ETL 0.16.0 in an isolated Python 3.13 environment on Windows.
- Actual PostgreSQL 16 container, reached through localhost port 5441.
- Docker Engine 27.0.3; PostgreSQL driver psycopg2-binary.
- The real Hydra CLI executed every job. No engine code was modified.

## Observed integration results

All targets initially contained exactly (1, 10) and (2, 20).
The same two-row CSV was loaded once into each of the three mode targets.

| Job | Actual Hydra exit code | Actual rows afterward | Exact values checked |
| --- | ---: | ---: | --- |
| append | 0 | 4 | (1,10), (2,20), (2,25), (3,30) |
| replace | 0 | 2 | (2,25), (3,30) |
| upsert | 0 | 3 | (1,10), (2,25), (3,30) |
| partial: append, atomic false | 1 | 202 | Original two rows plus all 200 rows from batches 1–2 |
| atomic: append, atomic true | 1 | 2 | Exactly the original two rows |

Both failures identified the intended PostgreSQL constraint
`lab11_quantity_nonnegative`. Only data row 201 has a negative quantity.
The helpers independently queried PostgreSQL and compared every retained ID and
quantity, not merely row counts. The final `check all` also passed.

An initial Windows output-encoding error occurred in the helper after the append
job had completed successfully and its evidence had been saved. The helper now
explicitly emits UTF-8. The saved successful append result was checked against
the database; the append job was not rerun against its changed table.

## Other completed checks

- All five generated jobs passed real `hdrctl validate`.
- The real CSV connector yielded four batches of 100, with the bad row first in batch 3.
- PostgreSQL atomic defaults checked through Hydra: replace true; append/upsert false.
- Checkers rejected an unrelated connection error, a falsely successful failure,
  wrong row counts, and altered values.
- Existing project overwrite protection passed.
- All six shell scripts passed Bash syntax checks.
- Docker Compose configuration validation passed.
- Startup-message tests passed: ready, failed, timeout, and missing resources.

## Startup correction — finalized 2026-11-07

The reported Killercoda session refused PostgreSQL connections on port 5441.
Its precise original cause was not established: no additional diagnostic commands
were requested after the user asked to avoid troubleshooting on Killercoda.

Startup now uses plain Docker through assets/start-database.sh, with no Compose
dependency. It waits for authenticated database access, seeds the five tables,
and verifies their contents before writing the ready marker. The foreground and
step 1 both wait explicitly; Check reports incomplete preparation instead of
silently failing. Existing database containers are never overwritten.

The corrected scripts were executed in a fresh local Ubuntu 24.04 container with
Python 3.12, Hydra 0.16.0, and an isolated Docker engine. Docker Compose was absent
and this absence was explicitly checked. The unmodified background script
installed Hydra, started PostgreSQL 16, seeded the tables, and reached Ready.

The following checks passed in that Linux environment:

- Foreground preparation and the step-1 readiness wait.
- All five actual loads: append 4 rows, replace 2, upsert 3, partial 202, atomic 2.
- Both intentional failures reported the expected PostgreSQL constraint error.
- All four step verification scripts (the scripts used by the Check buttons).
- Startup-message tests: ready, failed, timed out, and missing assets.
- Bash syntax for setup, asset, and step verification scripts.

## Scope and remaining validation

The corrected full startup and lesson flow passed locally under Linux. The updated
scenario has not been tested on Killercoda itself. No diagnostics or other actions
were performed on Killercoda during this repair. A fresh scenario session after
publication is required to receive the corrected startup assets.

Do not describe this as already tested on Killercoda. The whitebook placeholder
remains unchanged pending publication and learner testing.

Local integration evidence is retained in:
`C:\Users\DELL\.codex\visualizations\2026\10\29\01a1885f-418d-77e0-bb96-b6816681834f\lab11-live-project\evidence`.
