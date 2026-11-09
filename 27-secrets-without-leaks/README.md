# Lab 27 — Secrets without leaks

Killercoda lesson for [LAB lab-05-02] in 05-parameters-secrets.md.

The setup creates a disposable local PostgreSQL container, a random password in an ignored .hydra/secrets file, a two-row products table, and a Git repository in the learner project. The three stages run one Hydra database-to-CSV job with the secret from the project file, DB_PASSWORD, then a private file outside the project via --secrets-file.

The helper never prints or stores the password in a report. Its Check scripts inspect only the dedicated lesson project and its captured results. No Killercoda-wide probes or network scans are used.
