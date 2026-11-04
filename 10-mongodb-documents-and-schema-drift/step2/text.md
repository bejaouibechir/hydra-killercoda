# Compare warn and fail

**Expected behavior below is an acceptance target, not verified behavior in 0.16.0.**

Run the `warn` variant:

`/opt/hydra/bin/python /root/lab/lab10-resources/compare.py run warn`{{exec}}

The intended result is 102 rows with the original three columns, accompanied by a
warning identifying `sales_channel`. A successful exit alone is insufficient.

Inspect the second variant and run it:

`cat jobs/fail/sources.yaml`{{exec}}

`/opt/hydra/bin/python /root/lab/lab10-resources/compare.py run fail`{{exec}}

The intended result is a nonzero **Hydra** exit code identifying the unexpected
field, with no data rows committed for this one-batch exercise. The helper returns
success only when that expected rejection is observed. A connection failure does
not count as correct drift handling.

The helper invokes the real Hydra CLI. It records its exit code and complete output
under `evidence/`; it does not implement either policy itself.

`cat evidence/warn.json evidence/fail.json`{{exec}}
