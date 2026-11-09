# When things go wrong

Run a four-step Hydra workflow. Step B fails deliberately. Compare `on_failure: fail`, `skip` and `continue`, then add a retry policy with exponential backoff. You will edit one YAML file and read local JSON reports. No database, network call or external service is used by the workflow.

```text
       +--> B_fails --> D_after_B
A_start
       +--> C_independent
```

B and C are in the same parallel execution group. C may already have completed when B fails. With `fail`, Hydra stops before starting D. With `skip`, D is marked skipped. With `continue`, D runs despite B's failure.

Work in `/root/lab/when-things-go-wrong`. Wait for the **Ready** message before using **Check**.
