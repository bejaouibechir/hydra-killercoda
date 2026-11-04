# Fail at batch 3 without atomicity

The second file contains 400 rows. Hydra reads **100 rows per batch**. The quantity
at data row 201 (ID 1201) is -1, violating PostgreSQL's
`lab11_quantity_nonnegative` check constraint.

`/opt/hydra/bin/python /root/lab/lab11-resources/lab11.py show source`{{exec}}

`cat jobs/partial/sources.yaml jobs/partial/destinations.yaml`{{exec}}

This job uses `mode: append` and `atomic: false`. Batches 1 and 2 succeed.
The first row of batch 3 fails; batch 4 is never loaded.

`/opt/hydra/bin/python /root/lab/lab11-resources/exercise.py run partial`{{exec}}

`/opt/hydra/bin/python /root/lab/lab11-resources/lab11.py show partial`{{exec}}

Expected: **202 rows** — the 2 original rows plus the 200 rows committed by batches
1 and 2. The helper confirms every retained ID and quantity, and checks that Hydra
failed because of the deliberate database constraint.

**Hydra fails; the lesson check passes.** A missing dependency or a connection
error is not an acceptable substitute for the intended failure.
