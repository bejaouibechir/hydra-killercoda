# Lab 25 — Reversible actions

Killercoda lesson for [LAB lab-04-04] in 04-actions.md.

The learner writes a three-step rollback workflow. A Python action creates a local folder; a webhook action calls a receiver bound to 127.0.0.1:8790. Both have undo actions. An intentional failure triggers webhook cancellation and folder removal, in reverse order.

Setup installs hydra-etl==0.19.1, prepares /root/lab/reversible-actions, and starts the local receiver. The lesson requires no Docker, database, SSH or external webhook. The three checks inspect only the lesson files and evidence.
