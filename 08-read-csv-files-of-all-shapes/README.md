# 08 - Read CSV files of all shapes

Whitebook reference: **LAB lab-02-01**, chapter **02-jobs-part1.md**.

Status: **BLOCKED DRAFT - do not publish yet.** Hydra 0.16.0 ignores the CSV
`connection.delimiter` and `connection.encoding` settings used by this lesson.
Exercises 2 and 3 cannot pass after the documented corrections. See
[VERIFICATION.md](VERIFICATION.md) for the reproduced results and source findings.

Three guided exercises use the same three customer records: comma/UTF-8, semicolon/UTF-8, and semicolon/Latin-1. Names with accented characters make encoding mistakes observable.

## Content

- `assets/orders-*.csv`: the actual input files; the Latin-1 file is intentionally not UTF-8.
- `assets/lab08.py`: creates the jobs, records real CLI diagnostics and checks results.
- `setup/`: pinned Hydra installation and readiness reporting.
- `step*/`: English lesson and Killercoda Check hooks.
- `assets/editor.sh`, `assets/*.vsix`: editor support reused from lab 07.
- `tests/check_lab.py`: integration checks against the installed Hydra package.

The helper creates all three job manifests per job, shared data, output folders and corrected source manifests. No transformations are needed.

## Review locally

With Hydra 0.16.0 installed:

```bash
python tests/check_csv_settings.py
python tests/check_lab.py
```

Both commands currently return a failure: the first isolates the engine issue;
the second checks the intended complete lesson and stops at the corrected
semicolon case. They must pass against a fixed, published Hydra version before
the installation pin is updated and the lab is published.

For manual exploration, set `HYDRA_LAB08_ROOT` to a new or empty temporary directory, then run `python assets/lab08.py prepare`. Run the jobs from that directory. Use the same environment variable when invoking the helper.

Preparation refuses to overwrite a non-empty directory. `diagnose` runs a deliberately faulty job and records its actual output and exit code. It returns success only if the expected behavior was observed.

The semicolon mistake succeeds with one column; the encoding mistake fails. Checks require the observation, corrected settings and complete CSV values, then rerun the job.

## Platform review

Ubuntu provisioning and the Theia editor still require a real Killercoda test after publication is approved. Setup log: `/tmp/hydra-lab08-setup.log`.

Nothing is committed or pushed automatically.
