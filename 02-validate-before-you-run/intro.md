# Validate before you run

`hdrctl run` does not check your YAML before executing — it goes straight to the connector layer, and if something is wrong, you get whatever exception happens to surface. `hdrctl validate` does the opposite: it never touches a connector, it only cross-checks your YAML against itself, and it names problems precisely.

In this lab you will:

1. Scaffold a real, runnable job.
2. Break a source reference and run it anyway — see the raw failure.
3. Run `hdrctl validate` on the same broken job — see the clean failure.
4. Fix it, validate again, then run for real.

Hydra ETL installs in the background while you read this.
