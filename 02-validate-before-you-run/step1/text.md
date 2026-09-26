# Scaffold a working job

Create a job from the `csv` template — the only built-in template that ships with real sample data, so it can actually run end to end:

`hdrctl init brokenjob --template csv`{{exec}}

Look at what got created:

`find brokenjob -type f`{{exec}}

`cat brokenjob/pipeline.yaml`{{exec}}

`cat brokenjob/data/input.csv`{{exec}}

`pipeline.yaml` just says which source feeds which destination:

```yaml
pipeline:
  from: src_csv
  to: dest_csv
```

`src_csv` and `dest_csv` have to exist, spelled exactly like that, in `sources.yaml` and `destinations.yaml`. Next: what happens when they don't.
