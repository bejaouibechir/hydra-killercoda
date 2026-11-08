# Union another set of orders

`union` appends order 5. The secondary file repeats order 1, but `distinct: true` removes that identical row. Explain why there are five rows.

Study the YAML and the two CSV inputs, then run this job. You may edit `transformations.yaml` before running.

```bash
cd /root/lab/combine-data
cat jobs/stage3/sources.yaml
cat /root/lab/lab15-resources/stage3.yaml
cp /root/lab/lab15-resources/stage3.yaml jobs/stage3/transformations.yaml
hdrctl run jobs/stage3
cat output/stage3/result.csv
```

Explain each result row using the source IDs, then press **Check**. Your checked CSV is kept in `evidence/stage3.csv`.
