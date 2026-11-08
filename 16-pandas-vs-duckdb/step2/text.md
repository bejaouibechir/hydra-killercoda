# Force pandas

Study `jobs/pandas/transformations.yaml`. The job casts `amount` to float and sums it by country. The helper runs the real Hydra CLI with `--profile` and records elapsed time plus peak process memory.

```bash
cd /root/lab/engine-comparison
cat jobs/pandas/transformations.yaml
/opt/hydra/bin/python /root/lab/lab16-resources/benchmark.py run pandas
cat reports/pandas.json
```

Press **Check** after the run finishes.
