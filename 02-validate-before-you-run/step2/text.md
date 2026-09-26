# Break it, then run it

Introduce a realistic typo — the kind you get from renaming a source and missing one reference:

`sed -i 's/from: src_csv/from: src_csv_typo/' brokenjob/pipeline.yaml`{{exec}}

`cat brokenjob/pipeline.yaml`{{exec}}

Nothing stops you from running it anyway — `hdrctl run` does not validate first, it goes straight to execution:

`hdrctl run brokenjob`{{exec}}

You get a failure, but read it closely:

```
Pipeline FAILED in 0.0s

Cause:
ValueError: JobExecutor: source inconnue: 'src_csv_typo'
```

That's a raw internal exception leaking straight to your terminal — untranslated (notice it's in French, "source inconnue", even though the rest of the CLI is in English), naming an internal class (`JobExecutor`), with no pointer to *which file* to open. Workable if you already know the codebase. Not great otherwise.
