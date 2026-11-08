# Compare your two reports

```bash
cd /root/lab/engine-comparison
cat reports/pandas.json reports/auto.json
```

The selected engines should be pandas and duckdb, and both output files should contain the same four country totals. `wall_seconds` comes from the benchmark wrapper; `peak_rss_mib` is its sampled peak RSS. Hydra's `--profile` log records its own step timings and engine decision. Hardware and system load affect timings and memory.
