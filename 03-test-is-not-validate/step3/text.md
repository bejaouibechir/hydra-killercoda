# hdrctl validate agrees

`hdrctl validate dbjob`{{exec}}

```
DSL valid — no errors detected.
```

`validate` is even more static than `test` — it only checks the YAML's shape and that `pipeline.from`/`to` point at ids that exist. It never reads `.env` at all. Of course it passes: nothing here is actually wrong with the *files*.
