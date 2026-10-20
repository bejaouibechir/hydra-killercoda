# Scaffold a project and add a second job

Create a project — it comes with `job1` and `workflow1`:

`hdrctl init chainproject --template csv`{{exec}}

`job1` reads `data/input.csv`, keeps rows with `value > 0`, and writes `data/output.csv`. Add a `job2` that **reads job1's output** and keeps only the rows above 150. Start from a copy of `job1`:

`cp -r chainproject/jobs/job1 chainproject/jobs/job2 && rm chainproject/jobs/job2/data/input.csv chainproject/jobs/job2/README.md`{{exec}}

Point its source at `job1`'s output — the path is relative to `job2`'s own folder:

```
cat > chainproject/jobs/job2/sources.yaml <<'YAML'
sources:
  src_job1_output:
    type: csv
    extract:
      table: ../job1/data/output.csv
YAML
```{{exec}}

```
cat > chainproject/jobs/job2/pipeline.yaml <<'YAML'
pipeline:
  from: src_job1_output
  to: dest_csv
YAML
```{{exec}}

CSV values arrive as text, so cast `value` before comparing it:

```
cat > chainproject/jobs/job2/transformations.yaml <<'YAML'
steps:
  - cast:
      mapping:
        value: float
  - filter:
      expr: "value > 150"
YAML
```{{exec}}

`destinations.yaml` stays as copied: `job2` writes its own `data/output.csv`, inside `jobs/job2/`.

`find chainproject/jobs | sort`{{exec}}

When you are done, click **Check** to continue.
