# Verification

- `hdrctl trigger validate` must pass for both projects.
- With `hdrctl watch`, wait for a real `minute_clock` event, then add a new CSV; both must appear as successful `watch` runs, followed by `after_producer`.
- Stop watch, switch to the HTTP stage, launch `hdrctl serve` on localhost port 5683, call the webhook with curl, and check the producer and consumer histories.
- Check scripts only read the two lab project histories and configuration. They do not issue host diagnostics or unrelated commands on Killercoda.
