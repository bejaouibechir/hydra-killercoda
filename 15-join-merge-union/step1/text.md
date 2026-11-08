# Join orders with customer names

A left join keeps all four orders. C100 matches twice, C101 once, C102 has no customer name, and C103 has no order. Explain each resulting row.

Study the YAML and the two CSV inputs, then run this job. You may edit `transformations.yaml` before running.

```bash
cd /root/lab/combine-data
cat jobs/stage1/sources.yaml
cat /root/lab/lab15-resources/stage1.yaml
cp /root/lab/lab15-resources/stage1.yaml jobs/stage1/transformations.yaml
hdrctl run jobs/stage1
cat output/stage1/result.csv
```

Explain each result row using the source IDs, then press **Check**. Your checked CSV is kept in `evidence/stage1.csv`.
