# Repeat the failure with atomicity

The last job reads the identical 400-row file and writes to an untouched target
containing the same two original rows. Its load setting is `atomic: true`.

`cat jobs/atomic/destinations.yaml`{{exec}}

`/opt/hydra/bin/python /root/lab/lab11-resources/exercise.py run atomic`{{exec}}

`/opt/hydra/bin/python /root/lab/lab11-resources/lab11.py show atomic`{{exec}}

Expected: **2 rows**, exactly (1, 10) and (2, 20). PostgreSQL rolls back the entire
load, including the work from batches 1 and 2.

`/opt/hydra/bin/python /root/lab/lab11-resources/exercise.py check all`{{exec}}

| Experiment | Hydra outcome | Destination rows |
| --- | --- | ---: |
| append | Success | 4 |
| replace | Success | 2 |
| upsert | Success | 3 |
| append, atomic: false | Expected failure at batch 3 | 202 |
| append, atomic: true | Expected failure at batch 3 | 2 |

On a large append or upsert, `atomic: true` holds one transaction open for the
entire load. This can hold locks longer and increase database log pressure.
Atomicity is therefore off by default for these PostgreSQL modes. The deliberate
failure exercise uses append to isolate the transaction setting.

Each variant runs once. Start a fresh scenario to repeat the complete experiment;
the helpers refuse to silently reset or overwrite your results.
