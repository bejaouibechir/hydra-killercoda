# Lab 11 — Load modes and atomicity

Whitebook placeholder: **LAB lab-02-04**, chapter **02-jobs-part1.md**.

This local scenario uses Hydra 0.16.0 and a dedicated PostgreSQL 16 service.
Publication is subject to local review and explicit approval. See VERIFICATION.md
for the checks actually completed and any outstanding validation.

## Learning sequence

1. Inspect one CSV and five independent destination tables.
2. Load the same two CSV rows once with append, replace, and upsert.
3. Load a 400-row file with append and atomic disabled; fail at row 201.
4. Repeat against an untouched table with atomic enabled.

All tables start with (1, 10) and (2, 20). The normal input is (2, 25), (3, 30).
The append table permits duplicate IDs; the other tables have primary keys.
Failure tables additionally enforce quantity >= 0.

The failure file yields four batches of 100. Only data row 201 has quantity -1.
A real PostgreSQL check constraint rejects batch 3. Expected final row counts:
append 4, replace 2, upsert 3, partial 202, atomic 2.

## Resource layout

- `assets/`: CSV data, SQL fixture, Compose service, YAML templates, Python helpers.
- `setup/`: installation and progress/error reporting.
- `step1` through `step4`: English instructions and independent verification.
- `tests/check_offline.py`: manifest validation, actual CSV batch boundaries,
  default atomic settings, and checks against misleading results.

Setup installs Hydra with its PostgreSQL driver in /opt/hydra. Every lesson helper
uses /opt/hydra/bin/python explicitly, regardless of terminal activation.
It does not install an editor extension or restart editor processes.

## Local verification

Install `requirements.txt` in an isolated Python environment, then run:

```text
python -B tests/check_offline.py
docker compose -f assets/docker-compose.yml config --quiet
```

For a full test, start the Compose service, set HYDRA_LAB11_ROOT to a new disposable
project directory, and run with that same interpreter and environment:

```text
python -B assets/lab11.py prepare
python -B assets/lab11.py wait
python -B assets/lab11.py seed
python -B assets/exercise.py run append
python -B assets/exercise.py run replace
python -B assets/exercise.py run upsert
python -B assets/exercise.py run partial
python -B assets/exercise.py run atomic
python -B assets/exercise.py check all
```

The seed command refuses an existing lab11 schema. The run helper refuses a
previously run variant or altered baseline. There is no automatic reset of results.
Use a fresh disposable database/project to repeat the test.

The service binds only to 127.0.0.1:5441. Credentials are intentionally public demo
credentials for this dedicated lab, not production secrets. The prepared project
stores PG_PASSWORD in its ignored .hydra/secrets file.

Both intentionally failing Hydra commands must return nonzero. The helper succeeds
only when the expected constraint appears and the exact final rows are correct.
Evidence includes complete CLI logs, exit codes, and database rows.
