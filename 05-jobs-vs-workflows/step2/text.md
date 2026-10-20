# Jobs on their own: list, validate, run

The job commands see both jobs:

`hdrctl list chainproject/jobs`{{exec}}

```
  job1                           ✅ OK                        [transforms]
  job2                           ✅ OK                        [transforms]
```

`job2`'s YAML is consistent — its `pipeline.from` matches the ID in its `sources.yaml`:

`hdrctl validate chainproject/jobs/job2`{{exec}}

```
  ✅ DSL valid — no errors detected.
```

Now run it on its own:

`hdrctl run chainproject/jobs/job2`{{exec}}

```
  ❌ Pipeline FAILED
  ValueError: CSVConnector [src_job1_output]: Fichier source introuvable.
  Chemin demandé : ../job1/data/output.csv
```

It fails, and that's the point of this step. (The connector's detail message is in French: *source file not found*.) `job2` is valid, but it needs a file that only exists **after `job1` has run** — and `validate` cannot know that, because it checks the YAML, not the order in which things happen.

Ordering jobs is not a job's concern. It is what a workflow is for.

When you are done, click **Check** to continue.
