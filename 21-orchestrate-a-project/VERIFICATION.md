# Verification — LAB lab-03-04

Date: 2026-11-09. Local draft; no commit or push.

Tested with published hydra-etl[postgres]==0.19.1 and an isolated PostgreSQL 16 container. The learner thread was created from the exact YAML shown in step 1. The thread check passed: four primary workflows, a parallel sales/stock stage, one two-pass loop and a backup workflow outside the thread.

The normal project run passed with live PostgreSQL sales, one referentials run, two sales runs, two stock runs, one reports run and one loop event. After stopping the local database container, the second run passed with two source-availability fallback events and backup CSV sales. After restarting PostgreSQL, the third run passed with live sales again and no fallback. All four lesson checks passed.

The manifest references existing assets and steps; Python sources compiled in memory; all shell scripts passed bash -n. The disposable local test container was removed. Fresh Killercoda startup has not been tested. No Hydra engine files were modified.
