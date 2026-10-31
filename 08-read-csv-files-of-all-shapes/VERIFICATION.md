# Verification - blocked draft

Checked on 2026-10-31 against the published Hydra ETL 0.16.0 package on Windows.
The installed package was loaded from a separate validation environment.

## Actual CLI results

`python tests/check_csv_settings.py` runs five real jobs in a temporary folder:

| Case | Exit code | Result |
| --- | --- | --- |
| Comma / UTF-8, defaults | 0 | Correct: three columns, three rows, all values preserved |
| Semicolon / UTF-8, wrong default separator | 0 | Expected mistake: one column |
| Semicolon / UTF-8, corrected `connection.delimiter` | 0 | BLOCKED: still one column |
| Latin-1, default UTF-8 encoding | 1 | Expected UTF-8 decoding error |
| Latin-1, corrected delimiter and encoding | 1 | BLOCKED: still a UTF-8 decoding error |

## Cause observed in the source

`JobExecutor._build_connector` forwards the YAML settings under `config["connection"]`.
The CSV registry factory passes that dictionary unchanged to `CSVConnector`.
However, `CSVConnector._normalize_settings` reads `delimiter` and `encoding` only
from the top level of `config`. Consequently it uses comma and UTF-8 defaults.
`base_path` already has a nested-connection fallback, but these two options do not.
The same configuration path is present in the local Hydra source reviewed here.

No engine code, installed package, or CLI behavior was patched to hide this issue.

## Other checks completed

- Every scenario asset and lesson/script reference resolves.
- The Latin-1 fixture contains actual Latin-1 bytes and is not valid UTF-8.
- All three input fixtures represent the same logical records.
- Six Bash scripts pass `bash -n`, including the reused editor installer.
- The comma exercise passes its full output and rerun check.
- A missing output, the wrong separator, and stale one-column output are rejected.
- Preparation refuses to overwrite a non-empty lab directory.

The full lesson test stops at the corrected semicolon case. Its later checks
remain unvalidated until the engine issue is resolved. Ubuntu provisioning and
Theia installation also require a live Killercoda test after publication approval.

## Before publication

Resolve the engine issue in a separately authorized change, test a published
release containing the fix, update this lab's installation version and rerun
all checks. Keep the Whitebook placeholder until the lab works and is approved.
