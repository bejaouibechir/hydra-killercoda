# Verification — LAB lab-02-09

Date: 2026-11-08. Status: local draft ready for review.

The published hydra-etl 0.19.1 package was tested on a real, generated 5,000,000-row CSV (35,000,016 bytes). Hydra estimated 4,999,716 rows, above its default 2,000,000-row threshold. Both aggregation jobs completed and produced byte-identical four-row CSV files with country totals FR 12,500,000, BE 25,000,000, DE 37,500,000, ES 50,000,000 and 1,250,000 orders per country. The Check helper passed both variants.

On this Windows test host, the measured outcomes were:

| Variant | Selected engine | Wall time (s) | Sampled peak process RSS (MiB) |
| --- | --- | ---: | ---: |
| pandas | pandas | 9.856 | 365.9 |
| auto | duckdb | 10.192 | 642.8 |

These are local measurements, not promised performance on Killercoda. Hydra's `--profile` log recorded its own per-step timing and selected engine; memory came from `benchmark.py` sampling the child process RSS with psutil at 0.1-second intervals. That is an observed sample peak, not an exact operating-system high-water mark. The lab does not require DuckDB to be faster or use less memory; it checks engine selection and output parity.

The Killercoda manifest declares 12 assets and three steps. Five shell scripts and three Python scripts passed syntax checks. A clean Ubuntu/Killercoda startup remains untested locally. No Hydra engine files were changed; no commit or push was made.