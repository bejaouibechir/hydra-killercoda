# Verification

Checked locally on 2026-10-31 with the published `hydra-etl==0.16.0` package on Windows.

## Checks completed

`python tests/check_offline.py` passes:

- All assets, lesson pages and verification hooks referenced by `index.json` exist.
- The actual Hydra transformation engine produces all five expected IDs, names and totals from Decimal-valued source prices.
- The zero-quantity record remains with a zero total.
- An incorrect addition expression and a filter dropping the zero-total record are detected.
- Preparation refuses to overwrite a non-empty project.
- The missing transformation file is rejected.
- The complete manifests pass the real `hdrctl run jobs/products --dry-run`.
- The lesson checker rejects an incorrect total expression.

Seven Bash scripts pass `bash -n`. The Docker Compose file passes `docker compose config --quiet`.
Reader-facing text is English.

## Expected destination

| id | product_name | total |
| --- | --- | --- |
| 1 | Notebook | 50.00 |
| 2 | Keyboard | 59.85 |
| 3 | Monitor | 299.80 |
| 4 | USB cable | 0.00 |
| 5 | Mouse | 52.50 |

## Tests still required

**The actual database transfer has not been tested locally.** Docker's Linux engine
was unavailable, including after a background start attempt. No containers were
created and no existing database was modified.

`tests/check_live.py` is supplied for a host with Docker and both Python database
drivers. It requires an empty lab destination, tests both connections, confirms
that dry-run writes no rows, runs the job twice, compares every destination value,
and tests rejection of altered totals and names. These checks are pending, not
reported as passing.

The complete Ubuntu installation, container startup, SQL initialization, and
Theia extension also need a real Killercoda test after publication approval.

No Hydra engine code was changed. The earlier CSV lab's separate issue is outside
this SQL lab's scope.
