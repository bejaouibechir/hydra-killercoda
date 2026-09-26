# hdrctl test says everything passes

`hdrctl test dbjob`{{exec}}

Read the output carefully — two lines matter more than the rest:

```
src_mysql                           — mysql (connection not tested in test mode)
...
.env not found — ${ENV:...} variables will not be resolved
...
All tests pass — ready to execute.
```

`test` tells you, in its own output, that it did not test the connection and that your `.env` is missing — and still finishes with "All tests pass." Nothing here is hidden. It is just easy to skim past when the last line says "ready to execute."

When you are done, click **Check** to continue.
