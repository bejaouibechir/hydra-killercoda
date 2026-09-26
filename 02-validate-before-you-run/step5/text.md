# hdrctl run: see the result

It is now safe to run:

`hdrctl run brokenjob`{{exec}}

```
Pipeline completed successfully in 0.0s
  3 rows read
  3 rows written
```

`cat brokenjob/data/output.csv`{{exec}}

`pipeline.from`/`to` resolved, the `select` transform applied, real output written to disk — the same execution path `hdrctl validate` never touches, and the reason it is worth checking before you get here.

When you are done, click **Check** to continue.
