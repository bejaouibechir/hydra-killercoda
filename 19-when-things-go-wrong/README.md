# 19 — When things go wrong

Killercoda lab for `LAB lab-03-02` in `03-workflows.md`.

The user edits a four-step Hydra workflow, runs the real published `hydra-etl==0.19.1` runner for `fail`, `skip`, `continue` and exponential retry, then compares JSON reports. `B_fails` is an intentional local Python action failure. A and C succeed; D is absent with `fail`, skipped with `skip`, and successful with `continue`.

The setup uses the same asynchronous ready marker as lab 18. Killercoda Check scripts read only files inside this lab and do not contact external services. No commit or push is made by lab generation.
