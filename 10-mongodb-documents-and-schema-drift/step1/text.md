# Inspect documents and the inference sample

**Draft: perform these exercises only after the compatibility blocker is resolved.**

`cd /root/lab/mongodb-drift`{{exec}}

`/opt/hydra/bin/python /root/lab/lab10-resources/lab10.py show`{{exec}}

The helper checks that the collection has exactly 102 fixture documents and that
the 100-document inference sample contains no `sales_channel`. MongoDB does not
promise a natural order; the sample is checked again before every run.

Inspect the first variant:

`cat jobs/warn/sources.yaml`{{exec}}

- `mode: infer_strict` defines the intended infer-then-enforce behavior.
- `sample_size: 100` keeps the new field outside the inference sample.
- `drift_policy` controls the intended response when extraction encounters it.
- `batch_size: 1000` keeps this small exercise in one extraction batch.

All three jobs read the same collection. Each has its own output file.
