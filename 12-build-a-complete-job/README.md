# Lab 12 — Build a complete job

Whitebook note: LAB lab-02-05, chapter 02-jobs-part1.md.

Local draft for review. No publication is included in this change.

The learner creates four YAML manifests in an initially empty jobs/products
directory. A comma-separated CSV is read, quantity is cast to int, and the rows
are upserted into MySQL 8.4 using sku as the primary key.

First run: update SKU-001, insert SKU-002/SKU-003, preserve SKU-099.
Second run: change SKU-002 to Keyboard Pro, 34.95, quantity 7.
Both successful runs leave four rows; the checks compare all values.

## Startup

Hydra 0.19.1 and its MySQL driver are installed in /opt/hydra.
A dedicated MySQL container listens on localhost port 3313, started with plain
docker run. Compose is not used. Authenticated database access, seed rows, and
an empty job directory are checked before the ready marker is written.

The foreground script and step 1 wait for readiness. Every step's Check refuses
an incomplete or failed setup with a clear message. All helper commands explicitly
use /opt/hydra/bin/python. There are no extra diagnostic commands for learners.

The setup creates source data and demo secrets only; it does not create the four
job files. The solutions directory is for maintainers and is not deployed as a
Killercoda asset. Lesson commands create the files from scratch.

## Checks

- Step 1: source/transform parsing, input path, quantity cast.
- Step 2: all manifests, upsert key, source/destination IDs, real CLI validation.
- Step 3: exact MySQL values and saved first-run checkpoint.
- Step 4: updated source, previous checkpoint, exact second-run MySQL values.

The source-update helper requires the first-run result and refuses to overwrite
an already changed CSV. It preserves a backup and never writes to MySQL.

See VERIFICATION.md for the actual test environment and results.
