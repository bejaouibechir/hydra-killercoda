# Verification

## Interpreter correction

The live tutorial then failed with `No module named mysql` when a helper command
used system `python3`. SQL drivers are installed in `/opt/hydra`, and activation
inside the foreground setup script cannot be relied on in subsequent terminals.
All five clickable helper commands in steps 1 and 3 now explicitly invoke
`/opt/hydra/bin/python /root/lab/lab09-resources/lab09.py`.

Each replacement was checked, including preservation of the rest of both lesson
pages. This fixes the interpreter selection; the complete live transfer still
needs to be confirmed by the learner. No engine code or system Python was changed.
## Startup diagnostics update

The author's Killercoda session report confirmed that all lesson resources
arrived, the `sql-products` directory was created, and both database images
were downloaded. Those observations rule out a total asset-deployment failure.
A subsequent session report confirmed Hydra 0.16.0, both running containers and the readiness marker.

The setup now reports each stage, makes Python setup output unbuffered, names
missing assets, and displays the failed stage or last known status on timeout.
The introduction tells learners to wait for Ready and gives the exercise folder.

`python tests/check_setup_messages.py` passed four controlled Bash checks:
ready state, failure with logs, timeout with current stage, and missing asset.
Both edited setup scripts also passed Bash syntax checks. These tests do not
claim to reproduce or resolve an unconfirmed database failure in Killercoda.

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
