# Hydra DSL: the same result

Write `job/transformations.yaml` with clean, filter, window, cast, and aggregate steps. The source, destination and pipeline YAML files are already present. The numeric cast is necessary because the CSV has an empty amount.

```bash
cd /root/lab/three-ways
cat /root/lab/lab17-resources/transformations.solution.yaml
cp /root/lab/lab17-resources/transformations.solution.yaml job/transformations.yaml
hdrctl run job
cat output/hydra.csv
```

Compare the two rows with SQL and pandas, then press **Check**.
