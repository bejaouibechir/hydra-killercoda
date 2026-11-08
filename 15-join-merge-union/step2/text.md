# Merge order updates by ID

`merge` is keyed by order `id`: order 2 is replaced (amount 90, paid), order 5 is added, and orders 1, 3, 4 remain. Explain the five rows.

Study the YAML and the two CSV inputs, then run this job. You may edit `transformations.yaml` before running.

```bash
cd /root/lab/combine-data
cat jobs/stage2/sources.yaml
cat /root/lab/lab15-resources/stage2.yaml
cp /root/lab/lab15-resources/stage2.yaml jobs/stage2/transformations.yaml
hdrctl run jobs/stage2
cat output/stage2/result.csv
```

Explain each result row using the source IDs, then press **Check**. Your checked CSV is kept in `evidence/stage2.csv`.
