# What you observed

`fail` stops scheduling later groups; another step already running in B's parallel group can still finish. `skip` prevents B's dependent D from running while other branches proceed. `continue` lets D run despite B's failure. Retry attempts happen before the failure policy is applied; `max: 2`, `delay: 1`, `backoff: exponential` waits 1 and 2 seconds before giving up.

All three policies leave the workflow with errors because B failed. The four reports remain in `reports/` for comparison.
