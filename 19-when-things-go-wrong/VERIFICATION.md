# Verification — LAB lab-03-02

Date: 2026-11-09. Local draft; no commit or push.

Using the installed hydra-etl 0.19.1 package, I prepared a fresh learner directory and ran the actual WorkflowRunner four times. The `fail`, `skip`, `continue` and exponential `retry` reports all passed their respective lab checks. The failing action was deliberately local and invoked no external service.

Observed results: A and C succeeded in every run, B failed in every run; D was absent under `fail`, marked skipped under `skip`, and succeeded under `continue`. With `retry: {max: 2, delay: 1, backoff: exponential}`, B's logs showed waits of 1 and 2 seconds and then gave up after two retries; D ran because `on_failure: continue` was retained.

The manifest references existing assets and all four steps; Python sources compiled in memory. A Git Bash syntax command could not start in this environment, so Ubuntu/Killercoda startup remains untested. The Killercoda Check scripts only read files created by this lab. No engine files were modified.
