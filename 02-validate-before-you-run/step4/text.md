# hdrctl validate: the job is valid now

`hdrctl validate brokenproject/jobs/job1`{{exec}}

```
DSL valid — no errors detected.
```

Same command, same job, different result — because the only thing that changed is the one line `validate` was complaining about. Conclusion: `job1` is now valid.

When you are done, click **Check** to continue.
