# Read Hydra's error messages

A useful error message tells you **where the problem is, what is wrong and how to fix it**.

In this lab you will inspect a small workflow, diagnose three mistakes with `hdrctl run . --dry-run`, and correct one mistake at a time:

1. An unknown action: `webhok`.
2. An unknown key: `depend_on`.
3. A missing required field: `action`.

You will also check a different case: omitting `version` is **accepted**, not an error.

**Time:** about 12 minutes. **Prerequisites:** basic YAML indentation.

Hydra ETL 0.16.0 installs in the background. The project is created in `/root/lab/error-messages`. Each exercise starts from a fresh copy of its workflow.

All commands use **dry-run**. The webhook URL is a placeholder; no HTTP request is sent. There are no databases, credentials or input datasets to configure.
