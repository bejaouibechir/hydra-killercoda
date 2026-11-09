# 3. Continue: run the dependent step

Change B's policy to `continue` and run again:

```bash
cd /root/lab/when-things-go-wrong
sed -i 's/on_failure: skip/on_failure: continue/' workflow.yaml
/opt/hydra/bin/python /root/lab/lab19-resources/lab19.py run
cat reports/continue.json
```

B remains failed, but D now runs successfully. `continue` does not turn the failed action into a success. Press **Check**.
