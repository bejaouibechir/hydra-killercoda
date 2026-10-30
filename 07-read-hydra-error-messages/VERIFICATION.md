# Local verification

Date: 2026-10-30.

## Completed

- All 10 author tests passed against the local Hydra 0.16.0 implementation.
- All 10 author tests also passed against hydra-etl==0.16.0 downloaded from PyPI into a separate virtual environment. The CLI was resolved from that environment and ran in temporary project folders, not from the Hydra checkout.
- All 7 Bash scripts passed bash -n (syntax only).
- Every index.json resource reference resolves to an existing file.
- Text files use UTF-8 without BOM and LF line endings.
- The editor VSIX and extension installer were reused from existing lab 02.

The tests invoke the real hdrctl CLI with --dry-run. They check each expected failure, each correction and the accepted version omission. They also reject deleted steps, empty workflows, missing diagnostic evidence, mismatched exercises, stale evidence, malformed YAML and an added empty thread that would bypass the exercise.

Expected outcomes:

| Initial exercise | Exit code | After correction |
|---|---|---|
| unknown-action | 1 | 0 |
| unknown-key | 1 | 0 |
| missing-action | 1 | 0 |
| no-version | 0 | No correction needed |

The project remains limited to its marker and workflow file after diagnosis: no action is executed and no webhook is called.

Reproduce with Hydra 0.16.0 available on PATH:

```bash
python tests/check_lab.py
```

## Platform checks remaining

The Ubuntu provisioning script, Killercoda foreground interaction and Theia extension restart have not been executed on a live Killercoda instance. Local verification used Windows, Python 3.13 and Git Bash for shell syntax. A platform preview is still required after publication is approved.

## Delivery state

Only the new 07-read-hydra-error-messages directory was added to hydra-killercoda. Existing labs, the whitebook and Hydra engine source were not modified. The author has approved committing and pushing this lab for platform testing.
