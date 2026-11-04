# Lab 10 — MongoDB documents and schema drift

Whitebook placeholder: **LAB lab-02-03**, chapter **02-jobs-part1.md**.

**Status: BLOCKED DRAFT. Not ready for publication or learner testing.**

Hydra 0.16.0 drops the declared source schema at the executor/connector boundary.
Even with that schema supplied directly, the real MongoDB connector extracts all
102 fixture documents under every policy, without warning or rejection, and drops
the added field. The helpers do not patch or replace this behavior.

## Contents

- Three independent jobs generated from one YAML template, differing only in policy.
- 100 baseline documents plus two with a new `sales_channel` field.
- A dedicated MongoDB 7 container, bound to localhost port 27020.
- A guarded seed script, a real-CLI comparison helper, and three lesson steps.
- A compatibility probe that stops setup before downloading MongoDB on unsupported builds.
- Explicit Python interpreter paths in lessons and verification scripts.
- Offline checks and a verification report.

## Maintainer checks

In an isolated Python environment, install `requirements.txt`, then run:

```text
python -B tests/check_offline.py
python -B assets/probe.py
docker compose -f assets/docker-compose.yml config --quiet
```

The probe is expected to return **1** on 0.16.0; this is a reproduced blocker,
not a passing feature test. It uses the installed Hydra code and a small in-memory
cursor; it does not connect to MongoDB.

## Conditions for publication

1. Resolve schema forwarding and actual extraction-time drift handling in Hydra.
   No engine edits are part of this resource change.
2. Select a released build containing those fixes; update both requirements files.
3. Re-run the offline checks and probe, then the complete live scenario.
4. Confirm warning text, failure diagnostics, CSV columns, all source values, and
   preservation of `web` / `store` under adapt.
5. Review these draft expectations against the corrected engine contract.
6. Remove draft notices only after the checks pass and the content is approved.

Do not mark the whitebook placeholder complete or publish this scenario while blocked.
Do not bypass the startup probe to make the lab appear ready.

## Live validation after an engine fix

In a disposable Linux environment with Docker Compose, deploy `assets/*` to
`/root/lab/lab10-resources` and run the setup script, then follow the three steps.
The setup log is `/tmp/hydra-lab10-setup.log`.
Use a fresh lab instance if the fixture or a previous run's evidence has changed.
