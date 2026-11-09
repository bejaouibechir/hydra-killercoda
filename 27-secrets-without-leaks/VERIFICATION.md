# Verification

Local end-to-end test passed with a temporary PostgreSQL 16 container and Hydra 0.19.1. The same job read two rows using .hydra/secrets, DB_PASSWORD, and an external file passed with --secrets-file. Each stage reported a successful run, no password in Hydra output, and no secret file in git status.

The environment-variable Check was also run in a separate process without DB_PASSWORD, matching how Killercoda may launch a verification script. It passed using the saved run report. The test container was removed afterward.
