# 4. Retry with exponential backoff

Keep `on_failure: continue`. Add this block to `B_fails` at the same indentation level as `on_failure`:

```yaml
      retry:
        max: 2
        delay: 1
        backoff: exponential
```

`max: 2` means two retries after the first attempt. The waits are 1 second, then 2 seconds. Only after the third failure does Hydra apply `on_failure: continue` and start D.

```bash
cd /root/lab/when-things-go-wrong
/opt/hydra/bin/python /root/lab/lab19-resources/lab19.py run
cat reports/retry.json
```

Find `retry 1/2 in 1s`, `retry 2/2 in 2s`, and `gave up after 2 retry(ies)` in B's logs. Press **Check**.
