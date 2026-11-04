# Compare adapt and inspect the evidence

**Draft acceptance target:** retain the new field and all source rows.

`cat jobs/adapt/sources.yaml`{{exec}}

`/opt/hydra/bin/python /root/lab/lab10-resources/compare.py run adapt`{{exec}}

`head -n 3 jobs/adapt/output/orders.csv; tail -n 2 jobs/adapt/output/orders.csv`{{exec}}

The intended output has four columns: `_id`, `customer`, `amount`, and
`sales_channel`. The first 100 rows have an empty value in the last column;
ORD-101 contains `web`, and ORD-102 contains `store`.

`/opt/hydra/bin/python /root/lab/lab10-resources/compare.py check all`{{exec}}

| Policy | Intended result | New field |
| --- | --- | --- |
| warn | Complete with a drift warning | Omitted from the fixed output schema |
| fail | Stop with an explicit drift error | No successful output for this batch |
| adapt | Complete with an expanded output schema | Preserved |

These checks compare source values as well as row counts and column names.
Run each variant once in a fresh lab instance so stale output cannot hide a failure.
