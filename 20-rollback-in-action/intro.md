# Rollback in action

This lab uses one disposable PostgreSQL container and two tables, `lab20.invoices` and `lab20.payments`. Each starts with `(id=1, amount=100)`. Two Hydra jobs replace them with new CSV rows. A third action then fails deliberately.

With `rollback: true`, Hydra restores both original tables in reverse step order. You will then repeat the run with a simulated outside write to `payments`: automatic undo stops to protect that change. Remove only the lab's sentinel row and finish with `hdrctl workflow undo rollback_demo`.

Work only in `/root/lab/rollback-in-action`. Wait for **Ready** before starting; the initial installation can take several minutes. **Check** reads only this lab's two tables and local reports.
