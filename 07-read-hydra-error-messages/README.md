# 07 - Read Hydra's error messages

Whitebook reference: **LAB lab-01-02**, chapter **01-basics.md**.

Status: approved by the author for publication and testing on Killercoda.

## Scope

Four exercises, three deliberate errors, no workflow execution:

1. Unknown action (`webhok`).
2. Unknown key (`depend_on`).
3. Missing required `action` field.
4. Missing `version`: accepted by Hydra, with no error.

The third error replaces the original placeholder's mistaken assumption that a missing version is rejected. The whitebook itself has not been edited.

## Files

- `index.json`: Ubuntu scenario and uploaded assets.
- `intro.md`, `step*/text.md`, `finish.md`: English lesson.
- `setup/`: pinned Hydra 0.16.0 installation, readiness and failure reporting.
- `assets/*.yaml`: faulty exercises and the corrected reference.
- `assets/lab07.py`: prepare exercises, capture actual CLI diagnostics and check corrections.
- `step*/verify.sh`: Killercoda Check hooks.
- `assets/editor.sh`, `assets/*.vsix`: editor support reused from lab 02.

No CSV data is needed: this lab validates workflow structure, not a data job.

## Review locally

With Hydra 0.16.0 installed, set `HYDRA_LAB07_ROOT` to an **empty temporary directory** that already exists. Run:

```bash
python assets/lab07.py prepare unknown-action
python assets/lab07.py diagnose unknown-action
```

Edit `error-messages/workflows/errors.yaml` under that temporary directory, then run:

```bash
python assets/lab07.py check unknown-action
```

Repeat with `unknown-key` and `missing-action`. For `no-version`, diagnose and check without adding the version field.

`diagnose` invokes the real `hdrctl run . --dry-run`, displays its exit code and records the evidence. The helper itself returns 0 when the expected error was correctly recorded. It returns 1 for an unexpected result or an environment failure.

`prepare` resets only this lab's workflow and evidence for the selected exercise. `check` requires the intended manifest, saved diagnostic and a successful new dry-run. Deleting the faulty step or emptying the workflow does not pass.

## Platform review

The format follows [Killercoda's creator documentation](https://killercoda.com/creators). Full Ubuntu setup and the Theia extension must still be checked in a real Killercoda preview after the author approves publication. Setup logs: `/tmp/hydra-lab07-setup.log`; optional editor logs: `/tmp/hydra-lab07-editor.log`.

Do not run the workflow without `--dry-run`: its webhook URL is a deliberate placeholder.
