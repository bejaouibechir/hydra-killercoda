# 4. Retry with exponential backoff

Keep `on_failure: continue`. Add a `retry` block to `B_fails`. This terminal command makes the edit in your lab's `workflow.yaml`:

```bash
cd /root/lab/when-things-go-wrong
python3 - <<'PY'
from pathlib import Path

path = Path('workflow.yaml')
text = path.read_text()
anchor = '      on_failure: continue\n'
if anchor not in text:
    raise SystemExit('Set B_fails to on_failure: continue first')
if '\n      retry:\n' in text:
    raise SystemExit('retry already exists; inspect workflow.yaml')
block = '      retry:\n        max: 2\n        delay: 1\n        backoff: exponential\n'
path.write_text(text.replace(anchor, anchor + block, 1))
PY
grep -A5 'on_failure: continue' workflow.yaml
```

You should now see this block in the terminal:

```yaml
      on_failure: continue
      retry:
        max: 2
        delay: 1
        backoff: exponential
```

`max: 2` means two retries after the first attempt. Hydra waits 1 second and then 2 seconds. After the third failure, `on_failure: continue` lets D run.

```bash
/opt/hydra/bin/python /root/lab/lab19-resources/lab19.py run
cat reports/retry.json
```

The run must say `Written: /root/lab/when-things-go-wrong/reports/retry.json`. If it says `reports/continue.json`, the `retry` block is still missing from `workflow.yaml`. Find `retry 1/2 in 1s`, `retry 2/2 in 2s`, and `gave up after 2 retry(ies)` in B's logs, then press **Check**.
