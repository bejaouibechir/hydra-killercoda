# A project that runs itself

Two local Hydra projects: **producer** and **consumer**. A clock and a new file start producer. When producer ends successfully, consumer starts. You will watch those events in `hdrctl watch`, then call a real Hydra webhook on `127.0.0.1` with `curl`.

Hydra accepts project webhooks through `hdrctl serve`, not through `hdrctl watch`. The final step uses the same run history to inspect the HTTP event. All commands are confined to this lab and localhost. Wait for **Ready** before starting.
