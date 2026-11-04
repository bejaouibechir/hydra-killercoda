# Load the same file with three modes

Predict each result before running its job.

`/opt/hydra/bin/python /root/lab/lab11-resources/exercise.py run append`{{exec}}

`/opt/hydra/bin/python /root/lab/lab11-resources/lab11.py show append`{{exec}}

Append retains (1, 10) and (2, 20), then adds (2, 25) and (3, 30): **4 rows**.

`/opt/hydra/bin/python /root/lab/lab11-resources/exercise.py run replace`{{exec}}

`/opt/hydra/bin/python /root/lab/lab11-resources/lab11.py show replace`{{exec}}

Replace empties its target and loads only (2, 25) and (3, 30): **2 rows**.

`cat jobs/upsert/destinations.yaml`{{exec}}

Notice `mode: upsert` and `key: [id]`. The target has a matching primary key.

`/opt/hydra/bin/python /root/lab/lab11-resources/exercise.py run upsert`{{exec}}

`/opt/hydra/bin/python /root/lab/lab11-resources/lab11.py show upsert`{{exec}}

Upsert preserves (1, 10), changes ID 2 to quantity 25, and inserts (3, 30):
**3 rows**.

The helper invokes the real Hydra CLI and saves its complete output in
`evidence/<job>.log`. It checks database values through a separate connection.
It does not perform the load itself.
