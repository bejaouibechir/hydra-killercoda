# Restore a required field

Prepare the third exercise:

`python3 ../lab07-resources/lab07.py prepare missing-action`{{exec}}

`cat workflows/errors.yaml`{{exec}}

The `notify` step has `type: action`, but does not say which action to execute.

`python3 ../lab07-resources/lab07.py diagnose missing-action`{{exec}}

Look for:

```text
Step 'notify': type=action requires the 'action' field
Exit code: 1
```

Add `action: webhook` immediately below the `type: action` line of **notify**, using the same indentation. This command makes that specific edit:

```bash
python3 - <<'PY'
from pathlib import Path
p = Path('workflows/errors.yaml')
text = p.read_text()
old = '    - name: notify\n      type: action\n'
new = old + '      action: webhook\n'
assert text.count(old) == 1
p.write_text(text.replace(old, new))
PY
```{{exec}}

`hdrctl run . --dry-run`{{exec}}

A step name identifies the step. `type` selects job or action; `action` selects the action implementation. They are different fields.

Click **Check**.
