# Let hdrctl validate name the problem

Same broken job, different command:

`hdrctl validate brokenjob`{{exec}}

```
pipeline.from='src_csv_typo' not found in sources.yaml
...
1 error(s) detected.
```

No Python exception, no internal class name — just: this id, in this file, doesn't exist. `validate` never touches a connector and never executes anything; it only cross-checks the YAML against itself. That is exactly why it can afford to be this precise, and why running it costs nothing.
