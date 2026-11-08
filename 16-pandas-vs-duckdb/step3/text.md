# Let Hydra choose

The job differs only in `engine: auto`. Read the Hydra profile and the separate memory measurement, then compare them with pandas. Both jobs must produce the same four totals.

```bash
cd /root/lab/engine-comparison
cat jobs/auto/transformations.yaml
/opt/hydra/bin/python /root/lab/lab16-resources/benchmark.py run auto
cat reports/auto.json
cat reports/auto.log
```

Compare `wall_seconds` and `peak_rss_mib` between the JSON files. Performance varies with the machine; the Check button verifies engine selection and output equality, not that one run is faster.
