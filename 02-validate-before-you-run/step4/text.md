# Fix it, validate again, run for real

Put the correct id back:

`sed -i 's/src_csv_typo/src_csv/' brokenjob/pipeline.yaml`{{exec}}

`hdrctl validate brokenjob`{{exec}}

```
DSL valid — no errors detected.
```

Now it is actually safe to run:

`hdrctl run brokenjob`{{exec}}

`cat brokenjob/data/output.csv`{{exec}}

Rows in, rows out, `pipeline.from`/`to` resolved, the `select` transform applied, real output written to disk.
